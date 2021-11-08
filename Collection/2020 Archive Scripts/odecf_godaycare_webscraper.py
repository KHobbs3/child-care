"""
ODECF web scrapping script to scrape day care provider data
from www.godaycare.com.

Script scrapes the following data:
- Day care name
- Province/Territory Name
- City Name
- Address
- Day care age groups
- Day cate telephone number
"""

import csv
import requests
from bs4 import BeautifulSoup

DOMAIN = "http://www.godaycare.com"
ENCODING = "iso-8859-1"
OUTPUT_FILENAME = './output/odecf.csv'
USER_AGENT_HEADER = {
    'User-Agent': 'Robert Oikle, Statistics Canada',
    'From': 'robert.oikle@canada.ca'
}
CSV_DATA = []
DAY_CARE_NAME = ""
CITY_NAME = ""
PROV_TERR_NAME = ""
PROV_TERR_URLS = [
    "http://www.godaycare.com/alberta",
    "http://www.godaycare.com/british%20columbia",
    "http://www.godaycare.com/manitoba",
    "http://www.godaycare.com/new%20brunswick",
    "http://www.godaycare.com/newfoundland%20and%20labrador",
    "http://www.godaycare.com/northwest%20territories",
    "http://www.godaycare.com/nova%20scotia",
    "http://www.godaycare.com/nunavut",
    "http://www.godaycare.com/ontario",
    "http://www.godaycare.com/prince%20edward%20island",
    "http://www.godaycare.com/quebec",
    "http://www.godaycare.com/saskatchewan",
    "http://www.godaycare.com/yukon%20territory"
]


def request_page_source(prov_terr_url):
    """
    Request the page source for the prov/terr url
    """
    page_src = ""
    page_response = requests.get(prov_terr_url, timeout=5, headers=USER_AGENT_HEADER)
    if page_response.status_code == 200:
        page_src = page_response.content

    return page_src


def get_city_urls(bs):
    """
    Scrape a list of city URLs from a prov/terr page
    """
    global PROV_TERR_NAME
    PROV_TERR_NAME = ""

    heading = bs.find("div", class_="Heading")
    if heading:
        heading_h2 = heading.find('h2')
        if heading_h2:
            PROV_TERR_NAME = heading_h2.string[:-49]

    city_lists = bs.find_all('div', class_='menuCity')

    if city_lists:
        city_urls = []
        for city_list in city_lists:
            list_items = city_list.find_all('li')
            if list_items:
                for list_item in list_items:
                    list_item_link = list_item.find('a')
                    city_url = list_item_link.attrs['href']
                    if city_url:
                        city_urls.append(city_url)

    return city_urls


def request_city_page_source(city_source_url):
    """
    Get page source for the city page
    """
    city_url_fixed = city_source_url[11:].replace(' ', '%20')
    full_city_url = DOMAIN + city_url_fixed + '/1'
    city_page_src = ""
    city_page_response = requests.get(full_city_url, timeout=5, headers=USER_AGENT_HEADER)

    if city_page_response.status_code == 200:
        city_page_src = city_page_response.content

    return city_page_src


def get_city_day_care_urls(bs):
    """
    Scrape data related to city day care source
    - Get all city day care URLs
    - Get city name
    """
    dc_urls = []
    global CITY_NAME
    CITY_NAME = ""

    heading = bs.find('div', class_='Heading')
    if heading:
        heading_h2 = heading.find('h2')
        if heading_h2:
            CITY_NAME = heading_h2.string[36:]

    dc_links = bs.find_all('a', class_='dc_link')

    if dc_links:
        for dc_link in dc_links:
            dc_url = DOMAIN + dc_link.attrs['href'].replace(' ', '%20')
            dc_urls.append(dc_url)

    return dc_urls


def request_day_care_page_source(day_care_page_url):
    """
    Get the day care source page
    """
    dc_page_src = ""
    dc_page_response = requests.get(day_care_page_url, timeout=5, headers=USER_AGENT_HEADER)

    if dc_page_response.status_code == 200:
        dc_page_src = dc_page_response.content

    return dc_page_src


def get_day_care_details(bs):
    """
    Scrap specific details for day care
    Scraped Details:
    - Day care name
    - Day care province/territory
    - Day care city name
    - Day care location
    - Day care age groups
    - Day care phone number
    """
    global DAY_CARE_NAME
    DAY_CARE_NAME = ""

    dc_details = []

    # Get store day care name
    heading = bs.find('div', class_='Heading')
    if heading:
        heading_h2 = heading.find('h2')
        if heading_h2:
            DAY_CARE_NAME = heading_h2.string[:-34]
            dc_details.append(DAY_CARE_NAME.strip())

    # Store prov/terr name
    dc_details.append(PROV_TERR_NAME.strip())

    # Store city name
    dc_details.append(CITY_NAME.strip())

    # Information Div
    info_div = bs.find('div', id='InfoID')

    if info_div:
        # Store Location
        address = ""
        location = info_div.find('div', class_='InfoData')
        for content in location.contents:
            if str(content) == '<br/>':
                address += ' '
            else:
                address += content

        dc_details.append(address.strip())

        # Store Age Groups
        groups = info_div.find('div', class_='InfoDataWrap')
        if groups and groups.text:
            dc_details.append(groups.text.strip())
        else:
            dc_details.append('')

        # Store Telephone
        phone = info_div.find('div', class_='emphasis')
        if phone and phone.text:
            dc_details.append(phone.text.strip())
        else:
            dc_details.append('')

    print(dc_details)
    return dc_details


def write_csv_data(row_data):
    """
    Write scrapped data to a csv file
    """
    csv_header = ["Name", "Prov_Terr", "City", "Address", "Age_Groups", "Telephone"]
    with open(OUTPUT_FILENAME, 'w', encoding=ENCODING) as file:
        write = csv.writer(file)
        write.writerow(csv_header)
        write.writerows(row_data)

        file.close()


# Main web scrapping URL
for url in PROV_TERR_URLS:
    # Get page source
    src = request_page_source(url)

    # Create Beautiful Soup Object for Prov/Terr Page
    prov_terr_bs = BeautifulSoup(src, 'lxml')

    # Get list of city urls for the province or territory
    prov_terr_city_urls = get_city_urls(prov_terr_bs)

    # Loop through collected city urls
    for city in prov_terr_city_urls:
        city_src = request_city_page_source(city)

        # Create Beautiful Soup Object for City Page
        city_bs = BeautifulSoup(city_src, 'lxml')

        # Get City Day Care URLS
        day_care_urls = get_city_day_care_urls(city_bs)

        # Loop through day care urls
        for day_care_url in day_care_urls:
            # Request Day Care Source
            dc_src = request_day_care_page_source(day_care_url)

            # Create Beautiful Soup Object for Day Care Page
            dc_bs = BeautifulSoup(dc_src, 'lxml')

            # Get Day Care Details
            details = get_day_care_details(dc_bs)

            if details:
                CSV_DATA.append(details)

# Output CSV Data
write_csv_data(CSV_DATA)
