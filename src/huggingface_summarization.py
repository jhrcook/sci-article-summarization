"""Use the Bart transformer from Huggingface for text summarization."""

from typing import Any

from pydantic import BaseModel, PositiveFloat, PositiveInt
from transformers import pipeline

from src.text_utils import word_count


class HuggingFaceSummarizationConfiguration(BaseModel):
    """Configuration parameters for summarization with BART."""

    max_ratio: PositiveFloat = 0.3
    min_ratio: PositiveFloat = 0.1
    do_sample: bool = False
    early_stopping: bool = True
    length_penalty: PositiveFloat = 2.0
    no_repeat_ngram_size: PositiveInt = 3
    num_beams: PositiveInt = 4
    temperature: PositiveFloat = 1.0
    top_k: PositiveInt = 50
    top_p: PositiveFloat = 1.0


def _extract_summary(bart_res: Any) -> str:
    assert len(bart_res) == 1
    return bart_res[0]["summary_text"].strip()


def hugging_summarize(model: str, text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text with BART (from HuggingFace).

    Args:
        model (str): HuggingFace model identifier.
        text (str): Text to summarize.
        config_kwargs (dict[str, Any]): Configuration parameters.

    Raises:
        BaseException: Raised if there is an unexpected return type.

    Returns:
        str: Summary text.
    """
    config = HuggingFaceSummarizationConfiguration(**config_kwargs)
    summarizer = pipeline("summarization", model=model)
    n_words = word_count(text)
    res = summarizer(
        text,
        max_length=max(int(n_words * config.max_ratio), 100),
        min_length=max(int(n_words * config.min_ratio), 50),
        do_sample=config.do_sample,
        early_stopping=config.early_stopping,
        length_penalty=config.length_penalty,
        no_repeat_ngram_size=config.no_repeat_ngram_size,
        num_beams=config.num_beams,
        temperature=config.temperature,
        top_k=config.top_k,
        top_p=config.top_p,
    )
    return _extract_summary(res)


def bart_summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text with BART (from HuggingFace).

    Args:
        text (str): Text to summarize.
        config_kwargs (dict[str, Any]): Configuration parameters.

    Raises:
        BaseException: Raised if there is an unexpected return type.

    Returns:
        str: Summary text.
    """
    return hugging_summarize(
        model="facebook/bart-large-cnn",
        text=text,
        config_kwargs=config_kwargs,
    )


def t5_summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text with T5 (from HuggingFace).

    Args:
        text (str): Text to summarize.
        config_kwargs (dict[str, Any]): Configuration parameters.

    Raises:
        BaseException: Raised if there is an unexpected return type.

    Returns:
        str: Summary text.
    """
    return hugging_summarize(
        model="t5-base",
        text=text,
        config_kwargs=config_kwargs,
    )


def pegasus_summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text with Pegasus (from HuggingFace).

    Args:
        text (str): Text to summarize.
        config_kwargs (dict[str, Any]): Configuration parameters.

    Raises:
        BaseException: Raised if there is an unexpected return type.

    Returns:
        str: Summary text.
    """
    return hugging_summarize(
        model="google/pegasus-xsum",
        text=text,
        config_kwargs=config_kwargs,
    )
