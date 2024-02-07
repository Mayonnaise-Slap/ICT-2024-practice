from utils import get_soup
from bs4 import BeautifulSoup


def scrape_profile(profile_link: str) -> dict:
    profile_soup: BeautifulSoup = get_soup(profile_link)

    data = dict()

    data["tag"] = profile_soup.find(
        "a", {
            "class": "tm-user-card__nickname"
        }
    ).text.strip()
    data["karma"] = int(profile_soup.find("div", {"class": "tm-karma__votes"}).text)
    data["rating"] = float(profile_soup.find("span", {"class": "tm-votes-lever__score-counter"}).text)

    vals = profile_soup.find_all("dd")

    for i, tag in enumerate(profile_soup.find_all("dt")):
        match tag.string.strip():
            case "Специализация":
                data[tag.string.strip()] = {
                    vals[i].find("strong").string: list(
                        i.text for i in vals[i].find_all("div", {"class": "tm-user-specialization__skill"}))}
            case "Состоит в хабах":
                data[tag.string.strip()] = list(i.text for i in vals[i].find_all("a", {"class": "tm-user-hubs__hub"}))
            case "Подписан на компании":
                data[tag.string.strip()] = list(
                    i.text for i in vals[i].find_all("a", {"class": "tm-company-snippet__title"}))
            case "Дата рождения" | "Зарегистрирован":
                data[tag.string.strip()] = vals[i].find("time")["title"].split(", ")[0]
            case "Активность" | "Контактная информация" | "Приглашен":
                pass
            case _:
                data[tag.string.strip()] = vals[i].text.strip().replace("\xa0", " ")

    return data
