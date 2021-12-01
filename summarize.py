#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from pathlib import Path
from typing import Final, Optional, Union

from dotenv import load_dotenv
from typer import Typer

from src.parse_scientific_article import ScientificArticle, get_and_parse_article
from src.summarize_utils import (
    SummarizationConfiguration,
    SummarizationMethod,
    SummarizedScientificArticle,
    generate_configurations,
    get_urls,
    summarize_article,
)

# from src.write_summary import print_summary, write_summary

load_dotenv()

app = Typer()


@app.command()
def summarize_all() -> None:
    """Run the summarization pipeline to summarize a series of articles.

    Run the summarization pipeline to summarize a series of articles using different
    methods and configurations.
    """
    articles: list[ScientificArticle] = [
        get_and_parse_article(url) for url in get_urls()
    ]
    summarized_articles: list[SummarizedScientificArticle] = []
    for summ_config in generate_configurations():
        for article in articles:
            summarized_article = summarize_article(article, config=summ_config)
            summarized_articles.append(summarized_article)
    print(f"number of summarized articles: {len(summarized_articles)}")
    return None


@app.command()
def summarize(
    url: str,
    method: SummarizationMethod,
    output: Optional[Path] = None,
    ratio: Optional[float] = None,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
    temperature: Optional[float] = None,
) -> None:
    """Summarize an online scientific article.

    Args:
        url (str): URL of the webpage.
    """
    article = get_and_parse_article(url=url)
    kwargs = {
        "ratio": ratio,
        "min_ratio": min_ratio,
        "max_ratio": max_ratio,
        "temperature": temperature,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}  # remove Nones
    summarized_article = summarize_article(
        article,
        config=SummarizationConfiguration(method=method, config_kwargs=kwargs),
    )

    print(summarized_article)

    # if output is not None:
    #     write_summary(summarized_article, output)
    # else:
    #     print_summary(summarized_article)
    return None


KRAS_ALLELES_URL: Final[str] = "https://www.nature.com/articles/s41467-021-22125-z"


@app.command()
def make_examples() -> None:
    """Generate the example summarization results."""
    out_dir = Path("examples")
    if not out_dir.exists():
        out_dir.mkdir()

    configs: Final[dict[SummarizationMethod, dict[str, Union[float, str, bool]]]] = {
        SummarizationMethod.TEXTRANK: {"ratio": 0.2},
        # SummarizationMethod.BART: {"max_ratio": 0.2, "min_ratio": 0.1},
        # SummarizationMethod.GPT3: {
        #     "temperature": 0.3,
        #     "frequency_penalty": 0.1,
        #     "presence_penalty": 0.1,
        # },
    }

    for method, kwargs in configs.items():
        print(f"Summarizing with {method.value}")
        out_file = out_dir / f"kras-alleles-summary_{method.value}.md"
        summarize(
            KRAS_ALLELES_URL,
            method=method,
            output=out_file,
            **kwargs,
        )
        print(f"Results written to '{str(out_file)}'")
    return None


@app.command()
def parse_article(url: str) -> None:
    """CLI entrypoint to parse an article's webpage.

    Args:
        url (str): URL to an article's webpage.
    """
    article = get_and_parse_article(url=url)
    print(article)
    return None


if __name__ == "__main__":
    app()
