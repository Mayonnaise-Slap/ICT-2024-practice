import requests
from bs4 import BeautifulSoup
import re
import datetime
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


def get_article_text(article: BeautifulSoup) -> str:
    """
    This function takes a soup of an article on habr and
    returns the article in plain text. It does not save
    pictures or links, only plain text is returned.
    Args:
        article: A link to a habr article

    Returns:
    text (str): The article's plain text
    """

    return "\n".join(
        tag_contents.text.replace("&shy", "")
        .replace(";\xad", "")
        .replace("\xad", "")
        .replace("\xa0", " ")
        for tag_contents in article.find(
            "div", {"class": "article-formatted-body"}
        ).contents
    )


def get_article_attrs(article: BeautifulSoup) -> dict:
    """
    function takes a soup of an article on habr and
    returns the article's attributes that are listed
    on the top.
    Args:
        article (): soup of an article on habr

    Returns:
    dict with article attributes in a form
    {
    'Уровень сложности': 'Простой',
    'Время на прочтение': '8 мин',
    'Количество просмотров  69K': '69K',
    'other traits':
            ['Работа с видео',
            'Машинное обучение',
            'Искусственный интеллект',
            'Звук']
            }
    """
    article_tags = [
        n.text.strip(" *") for n in article.find_all(
            "a", {
                "class": "tm-publication-hub__link"
            })
    ]
    traits_soup = article.find_all(
        "div", {
            "class": "tm-article-snippet__stats"
        }
    )[0].find_all("span")

    trait_map = dict()

    for trait_id in range(len(traits_soup) // 2):
        trait = traits_soup[trait_id*2].title.text.strip()
        value = traits_soup[trait_id*2+1].text.strip()

        trait_map[trait] = value

    trait_map["tags"] = article_tags

    return trait_map


def scrape_article():
    """
        should return the article text, attributes and url's
        to the author's and commentators profiles
    """
    pass