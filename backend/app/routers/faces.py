import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import Face, Person, photo_persons
from ..schemas import FaceLabelRequest, FaceResponse

router = APIRouter(prefix="/faces", tags=["faces"])


@router.get("/photo/{photo_id}", response_model=List[FaceResponse])
def list_faces(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    faces = db.query(Face).filter(Face.photo_id == photo_id).all()
    return [FaceResponse.from_orm(f).copy(update={"person": f.person.display_name if f.person else None}) for f in faces]


@router.post("/{face_id}/label")
def label_face(face_id: uuid.UUID, payload: FaceLabelRequest, db: Session = Depends(get_db)):
    face = db.query(Face).filter(Face.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")

    person = db.query(Person).filter(Person.display_name == payload.display_name).first()
    if not person:
        person = Person(display_name=payload.display_name)
        db.add(person)
        db.commit()
        db.refresh(person)

    face.person_id = person.id
    db.add(face)

    # Propagate labels to similar faces using pgvector distance
    unlabeled_faces = (
        db.query(Face)
        .filter(and_(Face.person_id.is_(None), Face.id != face_id))
        .order_by(Face.embedding.op("<->")(face.embedding))
        .limit(50)
        .all()
    )

    threshold = 0.3
    labeled_count = 1
    for candidate in unlabeled_faces:
        distance = db.scalar(candidate.embedding.op("<->")(face.embedding))
        if distance is None or distance > threshold:
            continue
        candidate.person_id = person.id
        labeled_count += 1
        db.add(candidate)
        db.execute(
            insert(photo_persons).values(photo_id=candidate.photo_id, person_id=person.id)
            .on_conflict_do_nothing()
        )

    db.execute(insert(photo_persons).values(photo_id=face.photo_id, person_id=person.id).on_conflict_do_nothing())
    db.commit()

    return {"labeled": labeled_count, "person_id": person.id}
