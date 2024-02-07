from scrape_hub import get_page_urls
import multiprocessing as mp


if __name__ == '__main__':
    url = "https://habr.com/ru/hubs/machine_learning/articles/top/alltime/page{}/"
    params = list(url.format(i + 1) for i in range(2))

    p = mp.Pool()
    a = p.map(get_page_urls, params)
    p.close()
    p.join()

    print(a)
