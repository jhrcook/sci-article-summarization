"""Writing summarized articles to file."""

from pathlib import Path

from colorama import Fore, Style, init

from src.summarize_utils import SummarizationMethod, SummarizedScientificArticle

init(autoreset=True)


def _make_summary_file_name(article: SummarizedScientificArticle) -> str:
    ...


def write_summary(article: SummarizedScientificArticle, to_dir: Path) -> None:
    """Write a summary to file.

    TODO: implement
    """
    ...


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
