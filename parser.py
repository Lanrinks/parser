from bs4 import BeautifulSoup
import csv
URL = "https://www.kinopoisk.ru/premiere/ru/2021/"
FILE = 'movies.csv'


def save_file(items, path):
    with open(path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['name'], item['two'], item['three'], item['four'], item['five']])


def scroll():
    from selenium import webdriver
    import time

    chrome_driver = r"C:\chromedriver\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_driver)  # Call the browser
    browser.get(URL)

    ''' to auto scroll page '''
    SCROLL_PAUSE_TIME = 2.0
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = browser.page_source
    return html_source


def parse():
    html_source = scroll()
    soup = BeautifulSoup(html_source, "html.parser")

    items = soup.find_all('div', {'class': 'premier_item'})
    movie = []

    for item in items:
        a = item.find('div', {'class': 'textBlock'}).find('span')
        b = a.find_next_sibling("span")
        c = b.find_next_sibling("span")
        d = c.find_next_sibling("span")
        movie.append({
            'name': a.text,
            'two': b.text,
            'three': c.get_text(strip=True),
            'four': d.get_text(strip=True),
            'five': item.find('meta').get('content')

        })
    return movie


if __name__ == '__main__':
    movies = parse()
    save_file(movies, FILE)
