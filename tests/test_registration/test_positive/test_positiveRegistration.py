import sys
import os
#Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from main import generate_password as passw, generate_user_credentials as user
from utils import get_elements, click_element, filling_text
from main import url
user = user()
passw = passw()

class TestRegistration:
    @pytest.fixture()
    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #comment to open in browser
        self.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url + 'user/register')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        self.driver.quit()

    @allure.epic("Successful registration check")
    @allure.title("Registration test. Positive check")
    @allure.description("This test checks successful registration on the conduit.mate.academy website")
    def test_registration(self, setup):
        with allure.step('Fill the "Username" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Username']", user['username'])
        allure.attach(self.driver.get_screenshot_as_png(), name="Fill the 'Username' field")
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", user['email'])
        allure.attach(self.driver.get_screenshot_as_png(), name="Fill the 'Email' field")
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        allure.attach(self.driver.get_screenshot_as_png(), name="Fill the 'Password' field")
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")
        allure.attach(self.driver.get_screenshot_as_png(), name='click_on_signup',
                      attachment_type=allure.attachment_type.PNG)
        edit = get_elements(self.driver, "class", "ion-compose")[0]
        WebDriverWait(self.driver, 10).until(EC.visibility_of(edit))
        with allure.step('Check the successful registration'):
            assert self.driver.current_url == "https://conduit.mate.academy/"
            assert user['username'] == get_elements(self.driver, 'css', 'li.nav-item a.nav-link')[3].text
            assert EC.visibility_of(edit)
            assert ' Settings' == get_elements(self.driver, 'css', 'li.nav-item a.nav-link')[2].text
        allure.attach(self.driver.get_screenshot_as_png(), name="Assertion")