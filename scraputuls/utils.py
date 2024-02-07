import requests
from bs4 import BeautifulSoup


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
