"""Get and parse an online scientific article."""
import pickle
import re
from pathlib import Path
from typing import Optional, Union

import requests
from bs4 import BeautifulSoup, element
from pydantic import BaseModel

from src.text_utils import indent

section_text = list[str]
multisection_text = dict[str, list[str]]


class ScientificArticleText(BaseModel):
    """Organized text of a scientific article."""

    Abstract: section_text
    Introduction: section_text
    Methods: multisection_text
    Results: multisection_text
    Discussion: section_text

    def __str__(self) -> str:
        """Get a string representation of the scientific article text."""
        msg = f"Abstract: {len(self.Abstract)} paragraph(s)\n"
        msg += f"Introduction: {len(self.Introduction)} paragraph\n"
        msg += f"Methods: {len(self.Methods)} sections\n"
        msg += f"Results: {len(self.Results)} sections\n"
        msg += f"Discussion: {len(self.Discussion)} paragraph(s)"
        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article text."""
        return str(self)


class ScientificArticle(BaseModel):
    """Scientific article."""

    title: str
    url: str
    text: ScientificArticleText

    def __str__(self) -> str:
        """Get a string representation of the scientific article."""
        msg = self.title + "\n"
        msg += f"(url: {self.url})\n"
        msg += indent(str(self.text))
        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article."""
        return str(self)


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
    for possible_ref in soup.find_all("sup"):
        if possible_ref.find_all(id=re.compile("ref-link-section")):
            possible_ref.decompose()
    return None


def _extract_section_title(article_section: element.Tag) -> str:
    return article_section.find("h2").text.strip()


def _extract_section_text(article_section: element.Tag) -> section_text:
    return [x.text.strip() for x in article_section.find_all("p")]


def _extract_multisection_text(article_section: element.Tag) -> multisection_text:
    text: multisection_text = {}
    current_section_title: Optional[str] = None
    current_section: list[str] = []
    for section in article_section.find_all(["p", "h3"]):
        if section.name == "h3":
            if current_section_title is not None:
                assert len(current_section) > 0, "No text for section."
                text[current_section_title] = current_section
            current_section = []
            current_section_title = section.text.strip()
        else:
            current_section.append(section.text.strip())
    return text


def _extract_article_title(soup: BeautifulSoup) -> str:
    return soup.find(class_="c-article-title").text.strip()


def parse_article(res: requests.Response, url: str) -> ScientificArticle:
    """Parse an article into its major components.

    Args:
        res (requests.Response): Article webpage.

    Returns:
        ScientificArticle: Parsed article.
    """
    soup = BeautifulSoup(res.content, "html.parser")
    _remove_figures(soup)
    _remove_citations(soup)
    article_title = _extract_article_title(soup)
    article_sections = soup.find_all(class_="c-article-section")
    sections_dict: dict[str, Union[section_text, multisection_text]] = {}
    for section in article_sections:
        section_title = _extract_section_title(section)
        if re.findall("method|results", section_title.lower()):
            sections_dict[section_title] = _extract_multisection_text(section)
        else:
            sections_dict[section_title] = _extract_section_text(section)
    article_text = ScientificArticleText(**sections_dict)
    return ScientificArticle(title=article_title, url=url, text=article_text)


def get_and_parse_article(url: str) -> ScientificArticle:
    """Get and parse a scientific article from the web.

    Args:
        url (str): URL of the article.

    Returns:
        ScientificArticle: The data and text from the scientific article.
    """
    response = get_webpage(url=url)
    return parse_article(response, url=url)


# <h3 class="c-article__sub-heading" id="Sec3">
#   <i>KRAS</i> alleles are non-uniformly distributed across cancers
# </h3>
