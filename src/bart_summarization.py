"""Use the Bart transformer from Huggingface for text summarization."""

from typing import Any

from pydantic import BaseModel, PositiveInt
from transformers import pipeline


class BartSummarizationConfiguration(BaseModel):
    """Configuration parameters for summarization with BART."""

    max_length: PositiveInt = 200
    min_length: PositiveInt = 50
    do_sample: bool = False


def summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text with BART (from HuggingFace).

    Args:
        text (str): Text to summarize.
        config_kwargs (dict[str, Any]): Configuration parameters.

    Raises:
        BaseException: Raised if there is an unexpected return type.

    Returns:
        str: Summary text.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    config = BartSummarizationConfiguration(**config_kwargs)
    res = summarizer(
        text,
        max_length=config.max_length,
        min_length=config.min_length,
        do_sample=config.do_sample,
    )

    if (text_sum := res.get("summary_text")) is None:
        print(res)
        raise BaseException("BART failed unexpectedly.")

    return text_sum
