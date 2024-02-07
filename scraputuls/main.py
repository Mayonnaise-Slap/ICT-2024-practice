from scrape_hub import get_page_urls, get_number_of_pages, get_soup
import multiprocessing as mp
from itertools import chain


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


if __name__ == '__main__':
    url = "https://habr.com/ru/hubs/machine_learning/articles/top/alltime/"

    print(scrape_hub(url), 3)

