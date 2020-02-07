from selenium import webdriver
import pandas as pd


chrome_driver_path = r"C:\Users\P-P-H\Desktop\dev\booking\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)


def start_scraping():
    links = list()
    returned_data = list()
    hotel_data = list()
    hotel_fields = ["Staff", "Facilities", "Cleanliness", "Comfort", "Value Of Money", "Location", "Free Wifi"]
    driver.get("https://www.booking.com/")
    driver.find_element_by_name('ss').send_keys("beirut")  # Search
    driver.find_element_by_class_name('sb-searchbox__button').click()
    for i in driver.find_elements_by_class_name("sr-hotel__title"):
        links.append(i.find_element_by_class_name("hotel_name_link").get_attribute("href"))

    for url in links:
        driver.get(url)
        driver.find_element_by_id("js--hp-gallery-scorecard").find_element_by_class_name("big_review_score_detailed").click()
        for scores in driver.find_elements_by_class_name("c-score-bar__score"):
            hotel_data.append(scores.text)
        returned_data.append(dict(zip(hotel_fields, hotel_data)))
        hotel_data = []
    return pd.DataFrame(returned_data)

    # Testing Part
    # for i in links[:3]:
    #     driver.get(i)
    #     driver.find_element_by_id("js--hp-gallery-scorecard").find_element_by_class_name("big_review_score_detailed").click()
    #     for scores in driver.find_elements_by_class_name("c-score-bar__score"):
    #         hotel_data.append(scores.text)
    #     returned_data.append(dict(zip(hotel_fields, hotel_data)))
    #     hotel_data = []
    # return pd.DataFrame(returned_data)


if __name__ == '__main__':
    try:
        data = start_scraping()
        data.to_csv("test.csv", index=False)
    finally:
        driver.quit()

