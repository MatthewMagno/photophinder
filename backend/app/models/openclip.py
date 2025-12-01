"""Minimal OpenCLIP/SigLIP wrapper with lazy loading."""
from functools import lru_cache
from typing import List

import numpy as np


@lru_cache()
def get_model():
    # Stub: in production load actual OpenCLIP/SigLIP model
    return None


def encode_image(image) -> List[float]:
    _ = get_model()
    # Replace with actual embedding extraction
    return np.zeros(512, dtype=float).tolist()


def encode_text(text: str) -> List[float]:
    _ = get_model()
    return np.zeros(512, dtype=float).tolist()
