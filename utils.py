from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


def get_elements(driver, selector, value):
    if selector == "id":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, value))
        )
    elif selector == "name":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, value))
        )
    elif selector == "class":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, value))
        )
    elif selector == "tag":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, value))
        )
    elif selector == "link_text":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, value))
        )
    elif selector == "partial_link_text":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, value))
        )
    elif selector == "xpath":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, value))
        )
    elif selector == "css":
        return WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, value))
        )
    else:
        raise ValueError("Invalid selector type. Please use one of: 'id', 'name', 'class', 'tag', 'link_text', 'partial_link_text', 'xpath', 'css'.")


def click_element(driver, by, locator):
    elements = driver.find_elements(by, locator)
    for element in elements:
        element.click()


def filling_text(driver, selector, value, text):
    element = get_elements(driver, selector, value)[0]
    element.clear()
    element.send_keys(text)


def handle_alert(driver, accept=True):
    if accept:
        Alert(driver).accept()
    else:
        Alert(driver).dismiss()


def handle_modal_dialog(driver, accept=True):
    modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal")))
    if accept:
        modal.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    else:
        modal.find_element(By.CSS_SELECTOR, "button.btn-secondary").click()


def handle_dropdown(driver, selector, value, option_text):
    dropdown = get_elements(driver, selector, value)[0]
    dropdown.click()
    options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"{selector}[{value}] option"))
    )
    for option in options:
        if option.text == option_text:
            option.click()
            break

def press_tab_key(driver, selector_type, selector_value):
    element = None
    if selector_type == "css":
        element = driver.find_element(By.CSS_SELECTOR, selector_value)
    elif selector_type == "xpath":
        element = driver.find_element(By.XPATH, selector_value)
    elif selector_type == "id":
        element = driver.find_element(By.ID, selector_value)
    elif selector_type == "name":
        element = driver.find_element(By.NAME, selector_value)
    elif selector_type == "class":
        element = driver.find_element(By.CLASS_NAME, selector_value)
    elif selector_type == "link":
        element = driver.find_element(By.LINK_TEXT, selector_value)
    elif selector_type == "partial":
        element = driver.find_element(By.PARTIAL_LINK_TEXT, selector_value)

    element.send_keys(Keys.TAB)