"""Face detection/embedding stubs."""
from dataclasses import dataclass
from functools import lru_cache
from typing import List

import numpy as np


@dataclass
class FaceBox:
    x1: float
    y1: float
    x2: float
    y2: float


@lru_cache()
def get_models():
    # Load actual detection + embedding models in production
    return None


def detect_faces(image) -> List[FaceBox]:
    _ = get_models()
    # Return a single fake box to illustrate the flow
    width, height = image.size
    return [FaceBox(0.1 * width, 0.1 * height, 0.3 * width, 0.3 * height)]


def embed_face(cropped_face) -> List[float]:
    _ = get_models()
    return np.zeros(512, dtype=float).tolist()
