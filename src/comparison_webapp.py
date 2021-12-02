"""Components for the streamlit web application."""

import pickle
from pathlib import Path

import streamlit as st
from pydantic import BaseModel

from src.parse_scientific_article import multisection_text, section_text
from src.summarize_utils import SummarizationConfiguration, SummarizedScientificArticle


class SummarizedScientificArticleInfo(BaseModel):
    """Identifiable information of a article summary object."""

    title: str
    method: str
    config_str: str

    def __hash__(self) -> int:
        """Hash the identifiable information of an article summary.

        Returns:
            int: Hash value.
        """
        return hash(self.title + self.method + self.config_str)


def format_config(config: SummarizationConfiguration) -> str:
    """Format a configuration as a human-readable string.

    Args:
        config (SummarizationConfiguration): Summarization configuration.

    Returns:
        str: Human-readable string.
    """
    if (kwargs := config.config_kwargs) is None:
        return "Default configuration"
    return ", ".join(f"{k}: {v}" for k, v in kwargs.items())


def make_summary_info(
    article: SummarizedScientificArticle,
) -> SummarizedScientificArticleInfo:
    """Convert a summarized article object into an info object.

    Args:
        article (SummarizedScientificArticle): An article object.

    Returns:
        SummarizedScientificArticleInfo: An info object.
    """
    return SummarizedScientificArticleInfo(
        title=article.title,
        method=article.config.method.value,
        config_str=format_config(article.config),
    )


def read_summarization(fpath: Path) -> SummarizedScientificArticle:
    """Read in a summarized article object from pickle.

    Args:
        fpath (Path): Path to the pickled object.

    Returns:
        SummarizedScientificArticle: The summarized scientific article object.
    """
    with open(fpath, "rb") as file:
        article = pickle.load(file)
    return article


def write_article_section(text: section_text) -> None:
    """Write an article section to streamlit.

    Args:
        text (section_text): Article section.
    """
    text = [t for t in text if len(t) > 0]
    if len(text) == 0:
        st.write("(no text)")
    st.markdown("\n".join(text))
    return None


def write_article_multisection(text: multisection_text) -> None:
    """Write an article multi-section (e.g. Results section) to streamlit.

    Args:
        text (section_text): Article multi-section.
    """
    for sub_title, sub_text in text.items():
        st.markdown(f"**{sub_title}**")
        write_article_section(sub_text)
    return None


def get_summarized_articles(
    dir: Path,
) -> dict[SummarizedScientificArticleInfo, SummarizedScientificArticle]:
    """Read in the summarized article objects and format as a dictionary.

    Args:
        dir (Path): Directory holding the pickled summarized article objects.

    Returns:
        dict[SummarizedScientificArticleInfo, SummarizedScientificArticle]: Dictionary
        mapping summarization information to the full summary object.
    """
    files = [f for f in dir.iterdir() if f.suffix == ".pkl"]
    summaries = [read_summarization(f) for f in files]
    return {make_summary_info(a): a for a in summaries}


def more_info() -> str:
    """Get the more information string.

    Returns:
        str: More information about the project and application.
    """
    return """
    I wanted to experiment with various ML and AI summarization methods and thought that
    summarizing scientific articles would be an interesting task as they can be rather
    complicated and specialized.
    Therefore, I developed a pipeline to summarized a few scientific articles from the
    journal *Nature Communications* using different methods with a variety of
    configurations.
    I then developed this simple web application for the easy comparison of results.

    Below, you can select a scientific article and section of the article then two pairs
    of summarization methods and configurations.
    The summaries of the selected section by the two summarization
    methods/configurations are then presented side-by-side.

    The source code and more information about this project can be found in the GitHub
    repo, [jhrcook/sci-article-summarization]
    (https://github.com/jhrcook/sci-article-summarization), and any problems or
    questions can be left as an
    [Issue](https://github.com/jhrcook/sci-article-summarization/issues).
    """
