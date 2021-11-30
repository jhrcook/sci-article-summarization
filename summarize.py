#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from pathlib import Path
from typing import Optional

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
from src.write_summary import print_summary, write_summary

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
    progress_bar: bool = True,
    output: Optional[Path] = None,
) -> None:
    """Summarize an online scientific article.

    Args:
        url (str): URL of the webpage.
    """
    article = get_and_parse_article(url=url)
    summarized_article = summarize_article(
        article,
        config=SummarizationConfiguration(method=method),
        progress_bar=progress_bar,
    )

    if output is not None:
        write_summary(summarized_article, output)
    else:
        print_summary(summarized_article)
    return None


@app.command()
def parse_article(name: str, url: str) -> ScientificArticle:
    """CLI entrypoint to parse an article's webpage.

    Args:
        url (str): URL to an article's webpage.

    Returns:
        dict[str, list[str]]: Parsed article.
    """
    return get_and_parse_article(name=name, url=url)


if __name__ == "__main__":
    app()
