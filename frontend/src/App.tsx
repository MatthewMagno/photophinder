import React, { useEffect, useMemo, useState } from 'react'
import { buildImageUrl, fetchFaces, fetchPhotos, labelFace, searchPhotos, uploadPhoto, type Face, type Photo } from './api'

function GalleryCard({ photo, onClick }: { photo: Photo; onClick: () => void }) {
  return (
    <div className="card" onClick={onClick}>
      <img src={buildImageUrl(photo.thumb_key)} alt={photo.caption ?? 'Photo thumbnail'} />
      <div style={{ marginTop: '4px', color: '#475569', fontSize: '0.85rem' }}>
        {photo.caption ?? 'Processing...'}
      </div>
    </div>
  )
}

function FaceOverlay({ faces, onLabel }: { faces: Face[]; onLabel: (faceId: string, name: string) => void }) {
  const [active, setActive] = useState<string | null>(null)
  const [input, setInput] = useState('')

  return (
    <>
      {faces.map(face => (
        <div
          key={face.id}
          className="face-box"
          style={{
            left: face.bounding_box.x1,
            top: face.bounding_box.y1,
            width: face.bounding_box.x2 - face.bounding_box.x1,
            height: face.bounding_box.y2 - face.bounding_box.y1
          }}
          onClick={() => setActive(face.id)}
        >
          {active === face.id && (
            <div style={{ background: 'white', padding: '4px', marginTop: '-28px', borderRadius: '6px' }}>
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder={face.person_name ?? 'Name'}
                style={{ padding: '4px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
              />
              <button
                style={{ marginLeft: '4px', padding: '4px 8px' }}
                onClick={() => {
                  onLabel(face.id, input)
                  setActive(null)
                  setInput('')
                }}
              >
                Save
              </button>
            </div>
          )}
        </div>
      ))}
    </>
  )
}

export default function App() {
  const [photos, setPhotos] = useState<Photo[]>([])
  const [query, setQuery] = useState('')
  const [modalPhoto, setModalPhoto] = useState<Photo | null>(null)
  const [faces, setFaces] = useState<Face[]>([])

  useEffect(() => {
    fetchPhotos().then(setPhotos)
  }, [])

  useEffect(() => {
    if (!modalPhoto) return
    fetchFaces(modalPhoto.id).then(setFaces)
  }, [modalPhoto])

  const handleSearch = async () => {
    if (query.trim() === '') {
      fetchPhotos().then(setPhotos)
    } else {
      const results = await searchPhotos(query)
      setPhotos(results)
    }
  }

  const onUpload = async (file: File) => {
    const uploaded = await uploadPhoto(file)
    setPhotos(prev => [uploaded, ...prev])
  }

  const onFaceLabel = async (faceId: string, name: string) => {
    if (!name) return
    await labelFace(faceId, name)
    if (modalPhoto) {
      const refreshed = await fetchFaces(modalPhoto.id)
      setFaces(refreshed)
    }
  }

  const selectedImageUrl = useMemo(() => {
    if (!modalPhoto) return null
    return buildImageUrl(modalPhoto.preview_key)
  }, [modalPhoto])

  return (
    <div className="app-shell">
      <div className="gallery">
        {photos.map(photo => (
          <GalleryCard key={photo.id} photo={photo} onClick={() => setModalPhoto(photo)} />
        ))}
      </div>

      <div className="bottom-bar">
        <input
          type="text"
          placeholder="Search your photos..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter') handleSearch()
          }}
        />
        <button onClick={handleSearch}>Search</button>
        <label style={{ display: 'inline-block', background: '#10b981', padding: '0.75rem 1rem', borderRadius: '8px' }}>
          Upload
          <input type="file" accept="image/*" style={{ display: 'none' }} onChange={e => e.target.files && onUpload(e.target.files[0])} />
        </label>
      </div>

      {modalPhoto && selectedImageUrl && (
        <div className="modal" onClick={() => setModalPhoto(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div style={{ position: 'relative', display: 'inline-block' }}>
              <img src={selectedImageUrl} style={{ maxWidth: '80vw', borderRadius: '8px' }} />
              <FaceOverlay faces={faces} onLabel={onFaceLabel} />
            </div>
            <div style={{ marginTop: '8px', color: '#475569' }}>{modalPhoto.caption ?? 'Processing...'}</div>
          </div>
        </div>
      )}
    </div>
  )
}
