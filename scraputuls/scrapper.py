import requests
from bs4 import BeautifulSoup
import re
import datetime
from db import habr_news, session
import multiprocessing as mp


def get_soup(page_link: str) -> BeautifulSoup:
    """
    Standard requests+bs4 helper function
    Args:
        page_link: string url to a specific page
    Returns:
        BeautifulSoup of the page
    """
    r = requests.get(page_link)
    if r.status_code != 200:
        raise Exception(f"Something was wrong with the link {page_link}")
    return BeautifulSoup(r.text, "html.parser")


def get_article_text(article_link: str) -> str:
    """
    This function takes a link to an article on habr and
    returns the article in plain text. It does not save
    pictures or links, only plain text is returned.
    Args:
        article_link (): A link to a habr article

    Returns:
    text (str): The article's plain text
    """
    response = requests.get(article_link)
    if response.status_code != 200:
        raise Exception("foobar")
    soup = BeautifulSoup(response.text, "html.parser")

    return "\n".join(
        tag_contents.text.replace("&shy", "")
        .replace(";\xad", "")
        .replace("\xad", "")
        .replace("\xa0", " ")
        for tag_contents in soup.find(
            "div", {"class": "article-formatted-body"}
        ).contents
    )
