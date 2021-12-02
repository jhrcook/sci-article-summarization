"""Utilities for the main summarization script."""

from enum import Enum
from typing import Any, Callable, Final, Optional, Union

from pydantic.main import BaseModel

from src.bart_summarization import summarize as bart_summarize
from src.gpt3_summarization import summarize as gpt3_summarize
from src.pagerank_summarization import summarize as pagerange_summarize
from src.parse_scientific_article import (
    ScientificArticle,
    ScientificArticleText,
    multisection_text,
    section_text,
)
from src.text_utils import indent, word_count

article_type = dict[str, list[str]]
summarization_callable = Callable[[str, dict[str, Any]], str]


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


class SummarizationConfiguration(BaseModel):
    """Configuration for a summarization."""

    method: SummarizationMethod
    config_kwargs: Optional[dict[str, Union[float, str, bool]]] = None


class SummarizedScientificArticle(ScientificArticle):
    """The results of summarizing an article."""

    config: SummarizationConfiguration
    summary: ScientificArticleText

    def __str__(self) -> str:
        """Get a string representation of the scientific article summary."""
        msg = self.title + "\n"
        msg += f"(url: {self.url})\n"
        msg += "\n"
        msg += " Original text:\n"
        msg += indent(str(self.text))
        msg += "\n"
        msg += " Summarized text:\n"
        msg += indent(str(self.summary))

        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article summary."""
        return str(self)


SUMMARIZATION_CALLABLES: dict[SummarizationMethod, summarization_callable] = {
    SummarizationMethod.TEXTRANK: pagerange_summarize,
    SummarizationMethod.BART: bart_summarize,
    SummarizationMethod.GPT3: gpt3_summarize,
}

KEEP_SECTIONS = ["Introduction", "Results", "Discussion", "Results and discussion"]

SUMMARIZATION_METHOD_MAX_LENGTHS: Final[dict[SummarizationMethod, int]] = {
    SummarizationMethod.BART: 650,
    SummarizationMethod.GPT3: 650,
}


def _summarize(
    text: str, method: SummarizationMethod, kwargs: Optional[dict[str, Any]]
) -> str:
    fxn = SUMMARIZATION_CALLABLES.get(method)
    if kwargs is None:
        kwargs = {}
    if fxn is None:
        raise NotImplementedError(method.value)
    return fxn(text, kwargs)


def _compress_paragraphs(paragraphs: section_text, max_len: int) -> section_text:
    merged_p = ""
    new_ps: list[str] = []
    for p in paragraphs:
        if max_len < 0 or word_count(merged_p + " " + p) < max_len:
            merged_p += " " + p
        else:
            new_ps.append(merged_p)
            merged_p = p
    if len(merged_p) > 0:
        new_ps.append(merged_p)
    return new_ps


def _summarize_paragraphs(
    text: section_text,
    method: SummarizationMethod,
    max_len: int,
    kwargs: Optional[dict[str, Any]] = None,
) -> section_text:
    merged_text = _compress_paragraphs(text, max_len=max_len)
    summaries = [_summarize(t, method=method, kwargs=kwargs) for t in merged_text]
    return [" ".join(summaries)]


def _summarize_multisection_paragraphs(
    text: multisection_text,
    method: SummarizationMethod,
    max_len: int,
    kwargs: Optional[dict[str, Any]] = None,
) -> multisection_text:
    summaries: multisection_text = {}
    for title, paragraphs in text.items():
        summaries[title] = _summarize_paragraphs(
            paragraphs, method=method, max_len=max_len, kwargs=kwargs
        )
    return summaries


def summarize_article(
    article: ScientificArticle,
    config: SummarizationConfiguration,
) -> SummarizedScientificArticle:
    """Summarized an article.

    Args:
        url (str): URL for the article's webpage.
        article (parsed_article): The parsed article.
        config (SummarizationConfiguration): A configuration for the summarization
        method.

    Returns:
        SummarizedScientificArticle: The summarized article.
    """
    method = config.method
    max_len = SUMMARIZATION_METHOD_MAX_LENGTHS.get(config.method, -1)

    introduction_summary = _summarize_paragraphs(
        article.text.Introduction,
        method=method,
        max_len=max_len,
        kwargs=config.config_kwargs,
    )
    results_summary = _summarize_multisection_paragraphs(
        article.text.Results,
        method=method,
        max_len=max_len,
        kwargs=config.config_kwargs,
    )
    discussion_summary = _summarize_paragraphs(
        article.text.Discussion,
        method=method,
        max_len=max_len,
        kwargs=config.config_kwargs,
    )

    summarized_text = ScientificArticleText(
        Abstract=[],
        Introduction=introduction_summary,
        Methods=[],
        Results=results_summary,
        Discussion=discussion_summary,
    )
    return SummarizedScientificArticle(
        config=config, summary=summarized_text, **article.dict()
    )
