#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from enum import Enum
from typing import Any, Callable, Final, Optional

from dotenv import load_dotenv
from typer import Typer

from src.bart_summarization import BartSummarizationConfiguration
from src.bart_summarization import summarize as bart_summarize
from src.gpt3_summarization import Gpt3SummarizationConfiguration
from src.gpt3_summarization import summarize as gpt3_summarize
from src.pagerank_summarization import summarize as pagerange_summarize
from src.parse_scientific_article import get_and_parse_article, parsed_article

URL: Final[str] = "https://www.nature.com/articles/s41467-021-22125-z"

load_dotenv()

app = Typer()


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


summarization_callable = Callable[[str, dict[str, Any]], str]

summarization_callables: dict[SummarizationMethod, summarization_callable] = {
    SummarizationMethod.TEXTRANK: pagerange_summarize,
    SummarizationMethod.BART: bart_summarize,
    SummarizationMethod.GPT3: gpt3_summarize,
}


def _pre_summary_message(method: SummarizationMethod) -> None:
    method_msg = f"Summarization method: '{method.value}'"
    print(method_msg)
    print("=" * len(method_msg))
    return None


def _pre_section_message(name: str) -> None:
    print("\n" + name)
    print("-" * len(name))
    return None


@app.command()
def parse_article(url: str = URL) -> dict[str, list[str]]:
    """CLI to parse an article's webpage.

    Args:
        url (str, optional): URL to an article's webpage. Defaults to URL.

    Returns:
        dict[str, list[str]]: Parsed article.
    """
    return get_and_parse_article(url=url)


def _word_count(x: str) -> int:
    return len(x.split(" "))


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


def _summarize(
    method: SummarizationMethod, text: str, kwargs: Optional[dict[str, Any]] = None
) -> str:
    fxn = summarization_callables.get(method)
    if kwargs is None:
        kwargs = {}
    if fxn is None:
        raise NotImplementedError(method.value)
    return fxn(text, kwargs)


KEEP_SECTIONS = ["Introduction", "Results", "Discussion", "Results and discussion"]


def _preprocess_article(article: parsed_article, max_len: int = -1) -> parsed_article:
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


def _print_article(article: parsed_article) -> None:
    for title, text in article.items():
        print(f"{title}: {len(text)} ({[_word_count(t) for t in text]})")


@app.command()
def summarize(url: str) -> None:
    """Summarize an article from its webpage.

    Args:
        url (str): URL to the article's webpage.
    """
    for method in SummarizationMethod:  # [SummarizationMethod.GPT3]:
        max_len = summarization_method_max_lengths.get(method, -1)
        article = _preprocess_article(parse_article(url), max_len=max_len)
        _print_article(article)
        _pre_summary_message(method)
        for title, paragraphs in article.items():
            _pre_section_message(title)
            for paragraph in paragraphs:
                config_kwargs = _get_best_configuration_kwargs(method, paragraph)
                res = _summarize(method=method, text=paragraph, kwargs=config_kwargs)
                res = res.strip()
                if len(res) > 0:
                    print(res)
        print("-" * 80 + "\n")
    return None


if __name__ == "__main__":
    app()
