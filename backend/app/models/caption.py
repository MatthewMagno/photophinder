"""Captioning stub."""
from functools import lru_cache


@lru_cache()
def get_model():
    return None


def generate_caption(image) -> str:
    _ = get_model()
    return "A placeholder caption for the uploaded photo."
