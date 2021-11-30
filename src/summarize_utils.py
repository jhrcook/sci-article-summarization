"""Utilities for the main summarization script."""


from enum import Enum
from typing import Any, Callable, Final, Optional, Union

from pydantic.main import BaseModel

from src.bart_summarization import BartSummarizationConfiguration
from src.bart_summarization import summarize as bart_summarize
from src.gpt3_summarization import Gpt3SummarizationConfiguration
from src.gpt3_summarization import summarize as gpt3_summarize

# from src.pagerank_summarization import PageRankSummarizationConfiguration
from src.pagerank_summarization import summarize as pagerange_summarize
from src.parse_scientific_article import ScientificArticle, article_type


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


def _word_count(x: str) -> int:
    return len(x.split(" "))


# TODO: change the following function so that it augments a configuration instead of
# returning a novel one.


def _get_best_configuration_kwargs(
    method: SummarizationMethod, text: str
) -> dict[str, Any]:
    n_words = _word_count(text)
    if method is SummarizationMethod.BART:
        config = BartSummarizationConfiguration(
            max_length=int(n_words * 0.2), min_length=int(n_words * 0.05)
        )
        return config.dict()
    elif method is SummarizationMethod.GPT3:
        config = Gpt3SummarizationConfiguration(max_tokens=(n_words * 0.15))
        return config.dict()
    else:
        return {}


summarization_callable = Callable[[str, dict[str, Any]], str]

SUMMARIZATION_CALLABLES: dict[SummarizationMethod, summarization_callable] = {
    SummarizationMethod.TEXTRANK: pagerange_summarize,
    SummarizationMethod.BART: bart_summarize,
    SummarizationMethod.GPT3: gpt3_summarize,
}


def _summarize(
    method: SummarizationMethod, text: str, kwargs: Optional[dict[str, Any]] = None
) -> str:
    fxn = SUMMARIZATION_CALLABLES.get(method)
    if kwargs is None:
        kwargs = {}
    if fxn is None:
        raise NotImplementedError(method.value)
    return fxn(text, kwargs)


KEEP_SECTIONS = ["Introduction", "Results", "Discussion", "Results and discussion"]


def _preprocess_article(article: article_type, max_len: int = -1) -> article_type:
    # Filter for only certain sections.
    new_article = {k: t for k, t in article.items() if k in KEEP_SECTIONS}
    # Merge shorter paragraphs.
    for title, paragraphs in new_article.items():
        merged_p = ""
        new_ps: list[str] = []
        for p in paragraphs:
            if max_len < 0 or _word_count(merged_p + " " + p) < max_len:
                merged_p += " " + p
            else:
                new_ps.append(merged_p)
                merged_p = p
        if len(merged_p) > 0:
            new_ps.append(merged_p)
        new_article[title] = new_ps
    return new_article


summarization_method_max_lengths: Final[dict[SummarizationMethod, int]] = {
    SummarizationMethod.BART: 650,
    SummarizationMethod.GPT3: 1200,
}


def get_urls() -> set[str]:
    """Get the URLs for the articles to summarize.

    Returns:
        set[str]: Set of URLs.
    """
    return {"https://www.nature.com/articles/s41467-021-22125-z"}


class SummarizationConfiguration(BaseModel):
    """Configuration for a summarization."""

    method: SummarizationMethod
    config_kwargs: Optional[dict[str, Union[float, str, bool]]] = None


def generate_configurations() -> list[SummarizationConfiguration]:
    """Get configurations to use for the summarizations.

    Returns:
        list[SummarizationConfiguration]: List of summarization configurations.
    """
    textrank_ratios = [0.01, 0.05, 0.1, 0.2]
    return [
        SummarizationConfiguration(
            method=SummarizationMethod.TEXTRANK, config_kwarg={"ratio": ratio}
        )
        for ratio in textrank_ratios
    ]


class SummarizedScientificArticle(ScientificArticle):
    """The results of summarizing an article."""

    config: SummarizationConfiguration
    summary: article_type


def summarize_article(
    article: ScientificArticle, config: SummarizationConfiguration
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
    max_len = summarization_method_max_lengths.get(config.method, -1)
    article_text = _preprocess_article(article.text.copy(), max_len=max_len)
    summary_dict: article_type = {}
    for title, paragraphs in article_text.items():
        summarized_paragraphs: list[str] = []
        for paragraph in paragraphs:
            # config_kwargs = _get_best_configuration_kwargs(method, paragraph)
            res = _summarize(method=method, text=paragraph, kwargs=config.config_kwargs)
            res = res.strip()
            if len(res) > 0:
                summarized_paragraphs.append(res)
        summary_dict[title] = summarized_paragraphs
    return SummarizedScientificArticle(
        config=config, summary=summary_dict, **article.dict()
    )
