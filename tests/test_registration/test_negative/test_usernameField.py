import sys
import os
from selenium.common.exceptions import NoSuchElementException
#Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

class Test_Username_field_validation:
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

    @allure.epic("Username field validation")
    @allure.title("User can't register with a Username that start with digits")
    @allure.description("User can't register with a Username that start with digits")

    def test_invalid_username_start_digit(self, setup):
        with allure.step('Fill the "Username" field by data that start with digit'):
            filling_text(self.driver, "css", "input[placeholder='Username']", '1Username')
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", user['email'])
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element(
                'xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message_username not in error_message.text.strip():
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_space_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Something went wrong : {error_message.text}')
            elif error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_start_digit(setup)
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_space_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with the "Username" that start with digit ')

    @allure.epic("Username field validation")
    @allure.title("User can't register with a Username that contains spaces")
    @allure.description("User can't register with a Username that contains spaces")
    def test_invalid_username_with_space(self, setup):
        with allure.step('Fill the "Username" field by data that have spaces'):
            filling_text(self.driver, "css", "input[placeholder='Username']", 'user name')
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", user['email'])
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element(
                'xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message_username not in error_message.text.strip():
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_space_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Something went wrong : {error_message.text}')
            elif error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_space(setup)
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_space_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with the "Username" that contains spaces ')

    @allure.epic("Username field validation")
    @allure.title("User can't register with a Username that consists of 2 symbols")
    @allure.description("User can't register with a Username that consists of 2 symbols")
    def test_invalid_username_with_2_symbols(self, setup):
        short_name = generate_short_username()
        with allure.step('Fill the "Username" field by data that consists of 2 symbols'):
            filling_text(self.driver, "css", "input[placeholder='Username']", short_name)
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", user['email'])
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_2_symbols(setup)
            elif error_message.text.strip() == 'This email is taken.':
                self.test_invalid_username_with_2_symbols(setup)
            elif 'ion-compose' in error_message.get_attribute('class'):
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_2_symbols_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail('Test failed: "ion-compose" element is present on the page')
            elif error_message.text.strip() == 'Username must start with a letter, have no spaces, and be 3 - 40 characters.':
                pass
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_2_symbols_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Test failed: unexpected error message: "{error_message.text.strip()}"')
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_2_symbols_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with the "Username" that consists of 2 symbols ')

    @allure.epic("Username field validation")
    @allure.title("User can't register with a Username that consists of more tnah 40 symbols")
    @allure.description("User can't register with a Username that consists of more tnah 40 symbols")
    def test_invalid_username_with_more_than_40_symbols(self, setup):
        long_name = generate_long_username()
        with allure.step('Fill the "Username" field by data that consists of more than 40 symbols'):
            filling_text(self.driver, "css", "input[placeholder='Username']", long_name)
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", f"test{user['email']}")
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_more_than_40_symbols(setup)
            elif error_message.text.strip() == 'This email is taken.':
                self.test_invalid_username_with_more_than_40_symbols(setup)
            elif 'ion-compose' in error_message.get_attribute('class'):
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_more_than_40_symbols_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail('Test failed: "ion-compose" element is present on the page')
            elif error_message.text.strip() == 'Username must start with a letter, have no spaces, and be 3 - 40 characters.':
                pass
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_more_than_40_symbols_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Test failed: unexpected error message: "{error_message.text.strip()}"')
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_more_than_40_symbols_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with the "Username" that consists of more tnah 40 symbols')

    @allure.epic("Username field validation")
    @allure.title("User can't register with already-taken Username")
    @allure.description("User can't register with already-taken Username")
    def test_invalid_username_with_already_taken_username(self, setup):
        with allure.step('Fill the "Username" field by already-taken Username'):
            filling_text(self.driver, "css", "input[placeholder='Username']", random_username)
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", f"already{user['email']}")
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message.text.strip() == 'This username is taken.':
                pass
            elif error_message.text.strip() == 'This email is taken.':
                self.test_invalid_username_with_already_taken_username(setup)
            elif 'ion-compose' in error_message.get_attribute('class'):
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_already_taken_username_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail('Test failed: "ion-compose" element is present on the page')
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_already_taken_username_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Test failed: unexpected error message: "{error_message.text.strip()}"')
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_already_taken_username_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with already-taken Username')

    @allure.epic("Username field validation")
    @allure.title("User can't register with an empty 'Username' field")
    @allure.description("User can't register with an empty 'Username' field")
    def test_invalid_username_with_empty_username(self, setup):
        with allure.step('Leave the "Username" field empty'):
            filling_text(self.driver, "css", "input[placeholder='Username']", '')
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", f"already{user['email']}")
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element(
                'xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message_username not in error_message.text.strip():
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_empty_username',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Error message is wrong: {error_message.text}')
            elif error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_empty_username(setup)
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_empty_username',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with an empty Username field')

    @allure.epic("Username field validation")
    @allure.title("User can't register with a Username that contains special characters")
    @allure.description("User can't register with a Username that contains special characters")
    def test_invalid_username_with_special_characters(self, setup):
        with allure.step('Fill the "Username" field by data with special characters'):
            filling_text(self.driver, "css", "input[placeholder='Username']", generate_short_username() + 'te$t&^' )
        with allure.step('Fill the "Email" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Email']", f"special{user['email']}")
        with allure.step('Fill the "Password" field by generated valid data'):
            filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        with allure.step('Click on [Sign Up]'):
            click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")

        try:
            error_message = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ul/li/ul/li')
            if error_message.text.strip() == error_message_username:
                pass
            elif error_message.text.strip() == 'This username is taken.':
                self.test_invalid_username_with_special_characters(setup)
            elif error_message.text.strip() == 'This email is taken.':
                self.test_invalid_username_with_special_characters(setup)
            elif 'ion-compose' in error_message.get_attribute('class'):
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_special_characters_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail('Test failed: "ion-compose" element is present on the page')
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_special_characters_failed',
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f'Test failed: unexpected error message: "{error_message.text.strip()}"')
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name='test_invalid_username_with_special_characters_failed',
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail('Something went wrong. Maybe user is registered with the "Username" that contains special characters')

