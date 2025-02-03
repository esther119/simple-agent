from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    driver = webdriver.Chrome()
    return driver, WebDriverWait(driver, 10)


def safe_find_element(driver, by, value):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print(f"Error finding element {value}: {e}")
        return None
