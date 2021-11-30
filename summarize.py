#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from dotenv import load_dotenv
from typer import Typer

from src.parse_scientific_article import get_and_parse_article
from src.summarize_utils import (
    SummarizedArticle,
    generate_configurations,
    get_urls,
    summarize_article,
)

load_dotenv()

app = Typer()


@app.command()
def summarize() -> None:
    """Run the summarization pipeline to summarize a series of articles.

    Run the summarization pipeline to summarize a series of articles using different
    methods and configurations.
    """
    articles = {url: get_and_parse_article(url) for url in get_urls()}
    summarized_articles: list[SummarizedArticle] = []
    for summ_config in generate_configurations():
        for url, article in articles.items():
            summarized_article = summarize_article(url, article, config=summ_config)
            summarized_articles.append(summarized_article)
    return None


@app.command()
def parse_article(url: str) -> dict[str, list[str]]:
    """CLI entrypoint to parse an article's webpage.

    Args:
        url (str): URL to an article's webpage.

    Returns:
        dict[str, list[str]]: Parsed article.
    """
    return get_and_parse_article(url=url)


if __name__ == "__main__":
    app()
