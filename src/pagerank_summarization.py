"""Summarize text using the PageRank method."""

from summa import summarizer


def summarize(text: str, ratio: float = 0.2) -> str:
    """Summarize text using the PageRank method.

    Args:
        text (str): String to summarize.
        ratio (float, optional): How much to reduce the original text down to. Defaults
        to 0.2.

    Returns:
        str: Summary of the input text.
    """
    text_sum = summarizer.summarize(text, ratio=ratio)
    assert isinstance(text_sum, str), "Unexpected return type from summa library."
    return text_sum
