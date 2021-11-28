"""Summarization using GTP-3."""

import os
from typing import Any, Literal

import openai
from pydantic import BaseModel, PositiveInt
from pydantic.types import PositiveFloat

OpenaiGpt3Engine = Literal["davinci", "curie", "babbage", "ada"]


class Gpt3SummarizationConfiguration(BaseModel):
    """GPT-3 configuration parameters."""

    engine: OpenaiGpt3Engine = "davinci"
    temperature: PositiveFloat = 0.3
    max_tokens: PositiveInt = 150
    top_p: PositiveFloat = 1.0
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.1


def _openai_api_key() -> None:
    if (openai_key := os.getenv("OPENAI_API_KEY")) is None:
        raise BaseException("OpenAI API key not found.")
    openai.api_key = openai_key
    return None


def _text_to_gpt3_prompt(text: str) -> str:
    prefix = 'Summarize the following scientific article:\n"""\n'
    suffix = '\n"""\nSummary:\n"""\n'
    prompt = prefix + text + suffix
    return prompt


def _extract_gpt3_result(gpt3_response: dict) -> str:
    return gpt3_response["choices"][0]["text"]


def summarize(text: str, config_kwargs: dict[str, Any]) -> str:
    """Summarize text using GPT-3.

    Args:
        text (str): Input text.
        config_kwargs (dict[str, Any]): GPT-3 configuration parameters.

    Returns:
        str: Summarized test.
    """
    _openai_api_key()
    config = Gpt3SummarizationConfiguration(**config_kwargs)
    prompt = _text_to_gpt3_prompt(text)
    res = openai.Completion.create(prompt=prompt, **config.dict(), stop=['"""'])
    text_sum = _extract_gpt3_result(res)
    return text_sum
