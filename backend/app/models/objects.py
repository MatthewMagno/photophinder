"""Object detection stub."""
from typing import List


class DetectedObject(dict):
    label: str
    bbox: tuple
    score: float


def detect_objects(image) -> List[dict]:
    width, height = image.size
    return [
        {
            "label": "person",
            "bbox": (0.05 * width, 0.05 * height, 0.25 * width, 0.25 * height),
            "score": 0.9,
        }
    ]
