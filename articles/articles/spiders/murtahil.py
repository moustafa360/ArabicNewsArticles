from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


chrome_driver_path = r"C:\Users\P-P-H\Desktop\dev\booking\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path) # , chrome_options=options
columns = ["article_content", "Tags"]
website_link = "https://murtahil.com/health/"


def main():
    driver.get(website_link)
    links , article_content, tags, returned_data, temp = [], [], [], [], []

    load_more_articles = driver.find_element_by_class_name("show-more-button")

    while load_more_articles.is_enabled():
        load_more_articles.click()
        time.sleep(5)

    for link in driver.find_elements_by_class_name("more-link"):
        links.append(link.get_attribute("href"))

    for link in links:
        driver.get(link)

        article = driver.find_element_by_class_name("entry-content").text
        article = article.replace("\n", "")
        article_content.append(article)
        tags.append("صحة")
        temp.append("".join(article_content))
        temp.append("".join(tags))
        returned_data.append(dict(zip(columns, temp)))
        tags, temp, article_content = [], [], []
    return pd.DataFrame(returned_data)


if __name__ == '__main__':
    try:
        data = main()
        data.to_csv("alarabia_business.csv", encoding="utf-8", index=False)
    finally:
        driver.quit()
