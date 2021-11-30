"""Writing summarized articles to file."""

from pathlib import Path
from typing import Optional

from colorama import Fore, Style, init

from src.summarize_utils import SummarizationMethod, SummarizedScientificArticle

init(autoreset=True)


def make_summary_file_name(
    article: SummarizedScientificArticle, suffix: Optional[str] = ".md"
) -> str:
    """Make a file name for a summaried article.

    Args:
        article (SummarizedScientificArticle): Summarized article.
        suffix (Optional[str], optional): File suffix. Defaults to ".md".

    Returns:
        str: Custom file name based off of the article and summarization config.
    """
    fname: str = article.title.replace(" ", "-") + "_" + article.config.method.value
    if (kwargs := article.config.config_kwargs) is not None and len(kwargs) > 0:
        fname += "_".join([f"{k}-{v}" for k, v in kwargs.items()])
    if suffix is not None:
        fname += suffix
    return fname


def write_summary(article: SummarizedScientificArticle, to: Path) -> None:
    """Write a summary to file.

    Args:
        article (SummarizedScientificArticle): Summarized article.
        to (Path): File path.
    """
    text = "# " + article.title + "\n"
    text += "summarization method: " + article.config.method.value + "\n\n"
    for section_title, paragraphs in article.summary.items():
        text += "## " + section_title + "\n\n"
        text += "\n".join(paragraphs) + "\n"
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


def print_summary(article: SummarizedScientificArticle) -> None:
    """Print out a summarized article.

    Args:
        article (SummarizedScientificArticle): Summarized article information.
    """
    _pre_summary_message(name=article.title, method=article.config.method)
    for title, paragraphs in article.summary.items():
        _pre_section_message(title)
        print("\n".join(paragraphs))
    print("-" * 80 + "\n")
    return None
