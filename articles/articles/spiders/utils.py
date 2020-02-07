import time


def scrape_accommodation_data(driver, accommodation_url):
    driver.get(accommodation_url)
    accommodation_fields = dict()
    accommodation_fields['name'] = driver.find_element_by_id('hp_hotel_name') \
        .text.strip()

    # Get the accommodation score
    accommodation_fields['score'] = driver.find_element_by_class_name(
        'bui-review-score--end').find_element_by_class_name(
        'bui-review-score__badge').text

    # Get the accommodation location
    accommodation_fields['location'] = driver.find_element_by_id('showMap2') \
        .find_element_by_class_name('hp_address_subtitle').text

    # Get the most popular facilities
    accommodation_fields['popular_facilities'] = list()
    facilities = driver.find_element_by_class_name('hp_desc_important_facilities')
    for facility in facilities.find_elements_by_class_name('important_facility'):
        accommodation_fields['popular_facilities'].append(facility.text)

    return accommodation_fields


def scrape_results(driver, n_results):
    accommodations_urls = list()
    accommodations_data = list()

    for accomodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
        accommodations_urls.append(accomodation_title.find_element_by_class_name(
            'hotel_name_link').get_attribute('href'))

    # Iterate over a defined range and scrape the links
    for url in range(0, n_results):
        if url == n_results:
            break
        url_data = scrape_accommodation_data(driver, accommodations_urls[url])
        accommodations_data.append(url_data)
    return accommodations_data

