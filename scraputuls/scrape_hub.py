from scrapper import get_soup
from bs4 import BeautifulSoup


def get_number_of_pages(hub_soup: BeautifulSoup) -> int:
    return int(hub_soup.find_all(
        "a", {
            "class": "tm-pagination__page"
        }
    )[-1].text.strip())


def get_page_urls(hub_page_link: str) -> list[str]:
    try:
        hub_soup = get_soup(hub_page_link)
    except Exception:
        return []
    base_url = 'https://habr.com'

    data_links = list()

    for link in hub_soup.find_all('a', class_='tm-title__link'):
        href = link.get('href')
        data_links.append(base_url + href)

    return data_links


link = "https://habr.com/ru/hubs/machine_learning/articles/top/alltime/"
