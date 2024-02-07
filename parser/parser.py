from bs4 import BeautifulSoup
import requests


def get_article_links(url):
    base_url = 'https://habr.com'
    response = requests.get(url)
    data_links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = soup.find_all('a', class_='tm-title__link')
        for link in article_links:
            href = link.get('href')
            data_links.append(base_url + href)
    else:
        print(f'An error has occurred with status {response.status_code}')

    return data_links


def get_page_number(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_number = soup.find("div", {"class": "tm-pagination__pages"}).text
        return page_number.split()[3]
    else:
        return None


def main():
    url = 'https://habr.com/ru/hubs/machine_learning/articles/'
    article_links = get_article_links(url)
    page_number = get_page_number(url)

    print("article links:", article_links)
    print("page amount:", page_number)


if __name__ == "__main__":
    main()
