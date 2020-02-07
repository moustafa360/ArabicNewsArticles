from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


options = Options()
options.headless = True

chrome_driver_path = r"C:\Users\P-P-H\Desktop\dev\booking\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)  # , chrome_options=options

link = "https://www.alarabiya.net/ar/aswaq/oil-and-gas/archive/mainArea/0/mainContent/0/pArea75/0?&pageNo={}" # 502
columns = ["article_content", "Tags"]


def main():
    links, returned_data, article_content, tags, temp = [], [], [], [], []
    for num in range(1, 502):
        driver.get(link.format(num))
        links = []
        for i in driver.find_elements_by_class_name("article-card"):
            links.append(i.get_attribute("href"))
        for url in links:
            driver.get(url)
            try:
                driver.find_element_by_css_selector('.tags')
                article_content.append(driver.find_element_by_id("body-text").text)
                for x in driver.find_elements_by_css_selector('.tags a'):
                    tags.append(x.text.replace("#", ""))
                temp.append("".join(article_content))
                temp.append(" , ".join(tags))
                returned_data.append(dict(zip(columns, temp)))
                tags, temp, article_content = [], [], []
            except NoSuchElementException:
                pass
    return pd.DataFrame(returned_data)


if __name__ == '__main__':
    try:
        data = main()
        data.to_csv("alarabia_oil.csv", index=False)
    finally:
        driver.quit()