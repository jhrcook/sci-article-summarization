"""Writing summarized articles to file."""
from pathlib import Path

from src.summarize_utils import SummarizationMethod, SummarizedScientificArticle


def _make_summary_file_name(article: SummarizedScientificArticle) -> str:
    ...


def write_summary(article: SummarizedScientificArticle, to_dir: Path) -> None:
    """Write a summary to file.

    TODO: implement
    """
    ...


def _pre_summary_message(name: str, method: SummarizationMethod) -> None:
    method_msg = f"Summarizing '{name}' using '{method.value}'"
    print(method_msg)
    print("=" * len(method_msg))
    return None


def _pre_section_message(name: str) -> None:
    print("\n" + name)
    print("-" * len(name))
    return None


def print_summary(article: SummarizedScientificArticle) -> None:
    """Print out a summarized article.

    Args:
        article (SummarizedScientificArticle): Summarized article information.
    """
    _pre_summary_message(name=article.name, method=article.config.method)
    for title, paragraphs in article.summary.items():
        _pre_section_message(title)
        print("\n".join(paragraphs))
    print("-" * 80 + "\n")
    return None
