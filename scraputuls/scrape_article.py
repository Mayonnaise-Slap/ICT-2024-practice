from typing import Tuple

from utils import get_soup
from bs4 import BeautifulSoup


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
    trait_map = dict()
    try:
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

        for trait_id in range(len(traits_soup) // 2):
            trait = traits_soup[trait_id * 2].title.text.strip()
            value = traits_soup[trait_id * 2 + 1].text.strip()

            trait_map[trait] = value

        trait_map["tags"] = article_tags
        trait_map["creator"] = article.find("span", {"class": "tm-user-info__user"}).a["href"]
    except AttributeError:
        pass
    return trait_map


def get_comments_accounts(article_link: str) -> tuple:
    comments = get_soup(article_link + "comments/")
    return tuple(
        "https://habr.com" + p.a["href"] for p in comments.find_all(
            "span", {
                "class": "tm-user-info__user tm-user-info__user_appearance-default"
            }
        )
    )


def get_article_contents(url: str) -> tuple[dict, tuple]:
    soup = get_soup(url)
    result = get_article_attrs(soup)
    return result, get_comments_accounts(url)
