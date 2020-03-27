#!/usr/bin/env python3
#
# Prerequisites:
# 1) pip install selenium
# 2) chromedriver in path
from selenium import webdriver
import os
import json

BASE_URL = 'https://onemocneni-aktualne.mzcr.cz/covid-19'
RAW_DATA_PATH = './raw_data'


def main():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    try:
        for element in driver.find_elements_by_css_selector('div.visually-hidden'):
            attributes = get_attributes(driver, element)
            data_attribute = get_data_attribute(attributes)
            if data_attribute:
                name = attributes['id']
                data = attributes[data_attribute]
                json_data = json.loads(bytes(data, 'ascii').decode('unicode-escape'))
                filename = os.path.join(RAW_DATA_PATH, f"{name}.json")
                with open(filename, "w", encoding='utf8') as f:
                    f.write(json.dumps(json_data, ensure_ascii=False, indent=2))
    finally:
        driver.close()


def get_attributes(driver, element):
    return driver.execute_script("""
        var items = {};
        for (index = 0; index < arguments[0].attributes.length; ++index) {
            items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
        };
        return items;
    """, element)


def get_data_attribute(attributes):
    for key in attributes:
        if key.startswith('data-'):
            return key
    return None


if __name__ == "__main__":
    main()
