"""Summarize text using the PageRank method."""

from typing import Any

from pydantic import BaseModel
from summa import summarizer


class PageRankSummarizationConfiguration(BaseModel):
    """PageRank configuration parameters."""

    ratio: float = 0.2


def summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text using the PageRank method.

    Args:
        text (str): String to summarize.
        ratio (float, optional): How much to reduce the original text down to. Defaults
        to 0.2.

    Returns:
        str: Summary of the input text.
    """
    config = PageRankSummarizationConfiguration(**config_kwargs)
    text_sum = summarizer.summarize(text, ratio=config.ratio)
    assert isinstance(text_sum, str), "Unexpected return type from summa library."
    return text_sum
