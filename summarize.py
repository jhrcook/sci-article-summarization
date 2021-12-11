#!/usr/bin/env python3

"""Entrypoint to summarization functions."""

from itertools import product
from pathlib import Path
from typing import Final, Optional, Union

from dotenv import load_dotenv
from tqdm import tqdm
from typer import Typer, colors, secho

from src.classes_and_types import (
    ScientificArticle,
    SummarizationConfiguration,
    SummarizationMethod,
    SummarizedScientificArticle,
)
from src.parse_scientific_article import get_and_parse_article
from src.pipeline import generate_configurations, get_urls
from src.summarize_utils import summarize_article
from src.write_summary import make_summary_file_name, print_summary, write_summary

load_dotenv()

app = Typer()


def _write_summarized_article_to_json(
    article: SummarizedScientificArticle, path: Path
) -> None:
    with open(path, "w") as file:
        file.write(article.json())
    return None


@app.command()
def summarize_all(force: bool = False) -> None:
    """Run the summarization pipeline to summarize a series of articles.

    Run the summarization pipeline to summarize a series of articles using different
    methods and configurations.
    """
    outdir = Path("pipeline-results")
    if not outdir.exists():
        outdir.mkdir()

    articles: list[ScientificArticle] = [
        get_and_parse_article(url) for url in get_urls()
    ]
    configurations = generate_configurations()
    secho(f"number of articles: {len(articles)}", fg=colors.BLUE)
    secho(f"number of configurations: {len(configurations)}", fg=colors.BLUE)
    n_iters = len(articles) * len(configurations)
    n_summarizations_performed = 0
    for summ_config, article in tqdm(product(configurations, articles), total=n_iters):
        json_path = outdir / make_summary_file_name(
            article, summ_config, suffix=".json"
        )
        if force or not json_path.exists():
            summarized_article = summarize_article(article, config=summ_config)
            _write_summarized_article_to_json(summarized_article, json_path)
            n_summarizations_performed += 1
    secho(f"performed {n_summarizations_performed} summarizations")
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
    frequency_penalty: Optional[float] = None,
    presence_penalty: Optional[float] = None,
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
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}  # remove `None`s
    summarized_article = summarize_article(
        article,
        config=SummarizationConfiguration(method=method, config_kwargs=kwargs),
    )

    if output is not None:
        write_summary(summarized_article, output)
    else:
        print_summary(summarized_article)
    return None


KRAS_ALLELES_URL: Final[str] = "https://www.nature.com/articles/s41467-021-22125-z"


@app.command()
def make_examples() -> None:
    """Generate the example summarization results."""
    out_dir = Path("examples")
    if not out_dir.exists():
        out_dir.mkdir()

    configs: Final[dict[SummarizationMethod, dict[str, Union[float, str, bool]]]] = {
        SummarizationMethod.TEXTRANK: {"ratio": 0.1},
        # SummarizationMethod.BART: {"min_ratio": 0.1, "max_ratio": 0.3},
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
