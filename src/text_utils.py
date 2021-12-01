"""Utilities for text."""


def word_count(x: str) -> int:
    """Count words in text.

    Args:
        x (str): Text to count the words in.

    Returns:
        int: Number of words.
    """
    return len(x.split(" "))
