from utils import get_soup
from bs4 import BeautifulSoup


def scrape_profile(profile_link: str) -> dict:
    profile_soup: BeautifulSoup = get_soup(profile_link)

    data = dict()
    try:
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
                case "Подписан на компании" | "Подписана на компании":
                    tg = tag.string.strip()
                    if tg == "Подписана на компании":
                        tg = "Подписан на компании"
                    data[tg] = list(
                        i.text for i in vals[i].find_all("a", {"class": "tm-company-snippet__title"}))
                case "Дата рождения" | "Зарегистрирован" | "Зарегистрирована":
                    tg = tag.string.strip()
                    if tg == "Зарегистрирована":
                        tg = "Зарегистрирован"
                    data[tg] = vals[i].find("time")["title"].split(", ")[0]
                case "Активность" | "Контактная информация" | "Приглашен"| "Пригласил на сайт" | "Приглашена"| "Пригласила на сайт" :
                    pass
                case _:
                    data[tag.string.strip()] = vals[i].text.strip().replace("\xa0", " ")
    except AttributeError:
        pass
    return data
