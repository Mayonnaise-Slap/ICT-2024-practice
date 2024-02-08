from typing import Any

from scrape_hub import get_page_urls, get_number_of_pages, get_soup
from scrape_article import get_article_contents
from scrape_user import scrape_profile
import multiprocessing as mp
from itertools import chain
import sys
import json


sys.setrecursionlimit(25000)


def scrape_hub(url: str, n_pages: int = None) -> list:
    hub_soup = get_soup(url)
    url += "page{}/"

    if n_pages is None:
        n_pages = get_number_of_pages(hub_soup)

    parameters = list(url.format(i + 1) for i in range(n_pages))
    pool = mp.Pool()
    pool_result = pool.map_async(get_page_urls, parameters)
    pool.close()
    pool.join()

    return list(chain.from_iterable(pool_result.get()))


def scrape_article(urls: list) -> tuple[Any, Any]:
    pool = mp.Pool()

    contents = pool.map_async(get_article_contents, urls).get()
    pool.close()
    pool.join()

    return contents


def scrape_users(urls: list) -> dict:
    pool = mp.Pool()

    contents = pool.map_async(scrape_profile, urls)
    pool.close()
    pool.join()

    return contents.get()


if __name__ == '__main__':
    # url = "https://habr.com/ru/hubs/machine_learning/articles/top/alltime/"
    #
    # three_pages = scrape_hub(url, 2)
    # stuff = scrape_article(three_pages)
    #
    # articles, comments = [], []
    # for i,j in stuff:
    #     articles.append(i)
    #     comments.append(j)
    #
    # with open("../data/articles.json", "w") as f:
    #     json.dump(articles, f)
    #
    # with open("../data/comments.json", "w") as f:
    #     json.dump(list(chain.from_iterable(comments)), f)

    with open("../data/comments.json", "r") as f:
        a = json.loads(f.read())

    print(scrape_users(a[:500]))
