"""Writing summarized articles to file."""

from pathlib import Path
from typing import Optional

from colorama import Fore, Style, init

from src.summarize_utils import (
    ScientificArticle,
    SummarizationConfiguration,
    SummarizationMethod,
    SummarizedScientificArticle,
)

init(autoreset=True)


def make_summary_file_name(
    article: ScientificArticle,
    config: SummarizationConfiguration,
    suffix: Optional[str] = ".md",
) -> str:
    """Make a file name for a summaried article.

    Args:
        article (SummarizedScientificArticle): Summarized article.
        suffix (Optional[str], optional): File suffix. Defaults to ".md".

    Returns:
        str: Custom file name based off of the article and summarization config.
    """
    fname: str = article.title.replace(" ", "-") + "_" + config.method.value
    if (kwargs := config.config_kwargs) is not None and len(kwargs) > 0:
        fname += "_" + "_".join([f"{k}-{v}" for k, v in kwargs.items()])
    if suffix is not None:
        fname += suffix
    return fname


def write_summary(article: SummarizedScientificArticle, to: Path) -> None:
    """Write a summary to file.

    Args:
        article (SummarizedScientificArticle): Summarized article.
        to (Path): File path.
    """
    text = "# " + article.title + "\n\n"
    text += "summarization method: " + article.config.method.value + "\n\n"
    for section_title, paragraphs in article.summary.dict().items():
        if len(paragraphs) == 0:
            continue

        text += "## " + section_title + "\n\n"
        if isinstance(paragraphs, list):
            text += "\n".join(paragraphs) + "\n\n"
        elif isinstance(paragraphs, dict):
            for subsection, subparagraphs in paragraphs.items():
                text += "### " + subsection + "\n\n"
                text += "\n".join(subparagraphs) + "\n\n"
        else:
            raise BaseException("Unexpected type of paragraph in summary.")

    with open(to, "w") as file:
        file.write(text)
    return None


def _pre_summary_message(name: str, method: SummarizationMethod) -> None:
    name_msg = Fore.BLUE + Style.BRIGHT + f"'{name}'"
    method_msg = "  summarization method: " + method.value
    print(name_msg)
    print(method_msg)

    br_len = max(len(name_msg) - len(Fore.BLUE + Style.BRIGHT), len(method_msg))
    print("=" * br_len)
    return None


def _pre_section_message(name: str) -> None:
    print("\n" + Style.BRIGHT + name)
    print("-" * len(name))
    return None


def _pre_subsection_message(name: str) -> None:
    print("\n" + name)
    print("-" * len(name))
    return None


def _print_paragraphs(paragraphs: list[str]) -> None:
    print("\n".join(paragraphs))


def print_summary(article: SummarizedScientificArticle) -> None:
    """Print out a summarized article.

    Args:
        article (SummarizedScientificArticle): Summarized article information.
    """
    _pre_summary_message(name=article.title, method=article.config.method)
    for title, paragraphs in article.summary.dict().items():
        if len(paragraphs) == 0:
            continue
        _pre_section_message(title)
        if isinstance(paragraphs, list):
            _print_paragraphs(paragraphs)
        elif isinstance(paragraphs, dict):
            for subtitle, sub_paragraphs in paragraphs.items():
                _pre_subsection_message(subtitle)
                _print_paragraphs(sub_paragraphs)
        else:
            raise BaseException("Unexpected type of paragraph in summary.")
    print("-" * 80 + "\n")
    return None
