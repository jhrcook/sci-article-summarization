"""Get and parse an online scientific article."""
import pickle
import re
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup, element
from pydantic import BaseModel

article_type = dict[str, list[str]]


class ScientificArticle(BaseModel):
    """Scientific article."""

    name: str
    url: str
    text: article_type


def _get_url_cache_path(url: str) -> Path:
    return Path("cache") / re.sub(r"[^\w\s]", "", url)


def _check_cache(url: str) -> Optional[requests.Response]:
    cache_path = _get_url_cache_path(url)
    if not cache_path.exists():
        return None
    with open(cache_path, "rb") as file:
        res = pickle.load(file)
    return res


def _write_cache(url: str, res: requests.Response) -> None:
    with open(_get_url_cache_path(url), "wb") as file:
        pickle.dump(res, file=file)
    return None


def get_webpage(url: str) -> requests.Response:
    """Download an webpage and cache.

    Args:
        url (str): URL to the article.

    Raises:
        BaseException: Raised if the request fails.

    Returns:
        requests.Response: Request response.
    """
    if (res := _check_cache(url)) is not None:
        return res

    res = requests.get(url)

    if res.status_code != 200:
        raise BaseException(f"Page request failed ({res.status_code})")

    _write_cache(url=url, res=res)
    return res


def _remove_figures(soup: BeautifulSoup) -> None:
    fig_class = "c-article-section__figure js-c-reading-companion-figures-item"
    for div in soup.find_all(class_=fig_class):
        div.decompose()
    return None


def _remove_citations(soup: BeautifulSoup) -> None:
    for ref in soup.find_all(id=re.compile("ref-link-section")):
        ref.decompose()
    return None


def _extract_section_title(article_section: element.Tag) -> str:
    return article_section.find("h2").text


def _extract_section_text(article_section: element.Tag) -> list[str]:
    return [x.text for x in article_section.find_all("p")]


def parse_article(res: requests.Response) -> article_type:
    """Parse an article into its major components.

    Args:
        res (requests.Response): Article webpage.

    Returns:
        parsed_article: Parsed article.
    """
    keep_sections = {
        "Abstract",
        "Introduction",
        "Results",
        "Conclusion",
        "Discussion",
        "Methods",
    }

    soup = BeautifulSoup(res.content, "html.parser")
    _remove_figures(soup)
    _remove_citations(soup)
    article_sections = soup.find_all(class_="c-article-section")
    sections_dict: article_type = {}
    for section in article_sections:
        section_title = _extract_section_title(section)
        if section_title not in keep_sections:
            continue
        section_text = _extract_section_text(section)
        sections_dict[section_title] = section_text
    return sections_dict


def get_and_parse_article(name: str, url: str) -> ScientificArticle:
    """Get and parse a scientific article from the web.

    Args:
        url (str): URL of the article.

    Returns:
        ScientificArticle: The data and text from the scientific article.
    """
    response = get_webpage(url=url)
    return ScientificArticle(name=name, url=url, text=parse_article(response))
