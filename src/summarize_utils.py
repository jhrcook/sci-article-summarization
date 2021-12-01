"""Utilities for the main summarization script."""

from enum import Enum
from typing import Any, Callable, Final, Iterable, Optional, Union

from pydantic.main import BaseModel
from tqdm import tqdm

from src.bart_summarization import summarize as bart_summarize
from src.gpt3_summarization import summarize as gpt3_summarize
from src.pagerank_summarization import summarize as pagerange_summarize
from src.parse_scientific_article import ScientificArticle
from src.text_utils import word_count

article_type = dict[str, list[str]]


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


def _total_word_count(paragraphs: Iterable[Iterable[str]]) -> int:
    return sum(([sum([word_count(p) for p in ps]) for ps in paragraphs]))


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
            if max_len < 0 or word_count(merged_p + " " + p) < max_len:
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
    SummarizationMethod.GPT3: 650,
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


class MockProgressBar:
    """A mock progressbar class that does nothing."""

    def __init__(self) -> None:
        """Initialize a mock progressbar class that does nothing."""
        ...

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Do nothing."""
        ...

    def close(self) -> None:
        """Do nothing."""
        ...


def summarize_article(
    article: ScientificArticle,
    config: SummarizationConfiguration,
    progress_bar: bool = False,
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
    if progress_bar:
        total_article_length = _total_word_count(article_text.values())
        pbar = tqdm(total=total_article_length)
    else:
        pbar = MockProgressBar()

    for title, paragraphs in article_text.items():
        summarized_paragraphs: list[str] = []
        for paragraph in paragraphs:
            res = _summarize(method=method, text=paragraph, kwargs=config.config_kwargs)
            pbar.update(word_count(paragraph))
            res = res.strip()
            if len(res) > 0:
                summarized_paragraphs.append(res)
        summary_dict[title] = summarized_paragraphs
    pbar.close()
    return SummarizedScientificArticle(
        config=config, summary=summary_dict, **article.dict()
    )
