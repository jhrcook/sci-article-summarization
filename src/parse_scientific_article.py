"""Get and parse an online scientific article."""

import requests
from bs4 import BeautifulSoup, element


def get_article(url: str) -> requests.Response:
    """Download an article webpage.

    Args:
        url (str): URL to the article.

    Raises:
        BaseException: Raised if the request fails.

    Returns:
        requests.Response: Request response.
    """
    res = requests.get(url)
    if res.status_code == 200:
        return res
    raise BaseException(f"Page request failed ({res.status_code})")


def _extract_section_title(article_section: element.Tag) -> str:
    return article_section.find("h2").text


def _extract_section_text(article_section: element.Tag) -> str:
    return "\n".join([x.text for x in article_section.find_all("p")])


def parse_article(res: requests.Response) -> dict[str, str]:
    """Parse an article into its major components.

    Args:
        res (requests.Response): Article webpage.

    Returns:
        dict[str, str]: Parsed article.
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
    article_sections = soup.find_all(class_="c-article-section")
    sections_dict: dict[str, str] = {}
    for section in article_sections:
        section_title = _extract_section_title(section)
        if section_title not in keep_sections:
            continue
        section_text = _extract_section_text(section)
        sections_dict[section_title] = section_text
    return sections_dict


def get_and_parse_article(url: str) -> dict[str, str]:
    """Get and parse a scientific article from the web.

    Args:
        url (str): URL of the article.

    Returns:
        dict[str, str]: Parsed article.
    """
    response = get_article(url=url)
    article = parse_article(response)
    return article
