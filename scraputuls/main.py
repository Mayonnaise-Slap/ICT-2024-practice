from scrape_hub import get_page_urls, get_number_of_pages, get_soup
from scrape_article import get_article_contents
from scrape_user import scrape_profile
from itertools import chain
from typing import Any
import multiprocessing.dummy as mp
import numpy as np
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


if __name__ == "__main__":
    with open("../data/comments.json", "r") as f:
        data = json.load(f)

    users_data = list()

    for i, subset in enumerate(np.array_split(data, 50)):
        print(f"scraping {i+1} subset")
        try:
            user_subset = scrape_users(subset.tolist())
        except Exception as e:
            print(f"Failed batch {i+1}: {e}")
            continue

        users_data += user_subset

    with open("../data/users.json", "w") as users_file:
        json.dump(users_data, users_file, ensure_ascii=False, indent=4)
