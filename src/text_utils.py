"""Utilities for text."""

from typing import Iterable


def word_count(x: str) -> int:
    """Count words in text.

    Args:
        x (str): Text to count the words in.

    Returns:
        int: Number of words.
    """
    return len(x.split(" "))


def total_word_count(paragraphs: Iterable[Iterable[str]]) -> int:
    """Count the number of words in a list of paragraphs.

    Args:
        paragraphs (Iterable[Iterable[str]]): List of list of paragraphs.

    Returns:
        int: Number of words total.
    """
    return sum(([sum([word_count(p) for p in ps]) for ps in paragraphs]))


def indent(text: str, space: str = "  ") -> str:
    """Indent text.

    Args:
        text (str): Original text.
        space (str, optional): Indent to use. Defaults to "  ".

    Returns:
        str: Indented text.
    """
    _text = ""
    for line in str(text).strip().splitlines():
        _text += space + line + "\n"
    return _text
