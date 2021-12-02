"""Web application for comparing the different summarizations."""

from pathlib import Path
from typing import Final

import streamlit as st

from src.comparison_webapp import (
    SummarizedScientificArticleInfo,
    get_summarized_articles,
    more_info,
    write_article_multisection,
    write_article_section,
)

# --- Configure --- #

SUMMARIZATION_PIPELINE_OUTDIR: Final[Path] = Path("pipeline-results")

# ---- Setup ---- #


summ_articles = get_summarized_articles(SUMMARIZATION_PIPELINE_OUTDIR)


# ---- Streamlit app ---- #

st.title("Comparing scientific article summaries")

with st.expander("More info"):
    st.markdown(more_info())

article_infos = list(summ_articles.keys())

available_article_titles = list(set([a.title for a in article_infos]))
available_article_titles.sort()
article_title = st.selectbox("Choose an article", options=available_article_titles)

summarized_sections = ["Introduction", "Results", "Discussion"]
article_section = st.selectbox(
    "Choose a section of the article", options=summarized_sections
)

available_methods = list(set([a.method for a in article_infos]))
available_methods.sort()


for col_idx, col in enumerate(st.columns(2)):
    with col:
        _summ_method = st.selectbox(
            "Summarization method",
            options=available_methods,
            key=f"summ_method_{col_idx}",
        )
        _article_infos = [ai for ai in article_infos if ai.method == _summ_method]
        _summ_config = st.selectbox(
            "Configuration",
            options=[a.config_str for a in _article_infos],
            key=f"summ_config_{col_idx}",
        )
        _article_info = SummarizedScientificArticleInfo(
            title=article_title, method=_summ_method, config_str=_summ_config
        )
        _article = summ_articles[_article_info]

        if article_section == "Introduction":
            write_article_section(_article.summary.Introduction)
        elif article_section == "Discussion":
            write_article_section(_article.summary.Discussion)
        elif article_section == "Results":
            write_article_multisection(_article.summary.Results)
        else:
            st.write("Unexpected article seciton...")
