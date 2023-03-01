import sys
import os
from selenium.common.exceptions import NoSuchElementException
#Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
from selenium import webdriver
from main import generate_password as passw, generate_user_credentials as user, generate_short_username, generate_long_username
from utils import get_elements, click_element, filling_text, press_tab_key
from main import (
    generate_password,
    generate_user_credentials,
    url,
    error_message_username,
    error_message_already_taken_username,
    random_username,
    random_email,
)
user = user()
passw = passw()

class Test_Email_field_validation:
    @pytest.fixture()
    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #comment to open in browser
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url + 'user/register')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        self.driver.quit()

    @allure.epic("Email field validation")
    @allure.title("User can't register with already-taken Email")
    @allure.description("User can't register with already-taken Email")
    def test_invalid_username_with_already_taken_email(self, setup):
        with allure.step('Fill the "Username" field by generated Username'):
            filling_text(self.driver, "css", "input[placeholder='Username']", user['username'])
        with allure.step('Fill the "Email" field by already-taken email'):
            filling_text(self.driver, "css", "input[placeholder='Email']", random_email)
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message.text.strip() == 'This email is taken.':
                pass
            elif error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_already_taken_email(setup)
            elif 'ion-compose' in error_message.get_attribute('class'):
                allure.attach(self.driver.get_screenshot_as_png(),
                              name='test_invalid_username_with_already_taken_username_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail('Test failed: "ion-compose" element is present on the page')
            else:
                allure.attach(self.driver.get_screenshot_as_png(),
                              name='test_invalid_username_with_already_taken_username_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Test failed: unexpected error message: "{error_message.text.strip()}"')
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name='test_invalid_username_with_already_taken_username_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with already-taken Username')
