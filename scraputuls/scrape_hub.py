from scrapper import get_soup
from bs4 import BeautifulSoup
import multiprocessing as mp


def get_number_of_pages(hub_soup: BeautifulSoup) -> int:
    return int(hub_soup.find_all(
        "a", {
            "class": "tm-pagination__page"
        }
    )[-1].text.strip())


def get_page_urls(hub_page_link: str) -> list[str]:
    hub_soup = get_soup(hub_page_link)
    base_url = 'https://habr.com'

    data_links = list()

    for link in hub_soup.find_all('a', class_='tm-title__link'):
        href = link.get('href')
        data_links.append(base_url + href)

    return data_links


def scrape_hub(url: str) -> list[str]:
    n_pages = get_number_of_pages(get_soup(url))
    url += "page{}/"

    results = list()

    pool = mp.Pool()


    get_page_urls(
        get_soup(
            url.format(1)
        )
    )

    return results


if __name__ == '__main__':
    scrape_hub("https://habr.com/ru/hubs/machine_learning/articles/top/alltime/")

