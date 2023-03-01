import sys
import os
# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from userdata.generate_data import generate_password as passw, generate_user_credentials as user
from utils import get_elements, click_element, filling_text
from userdata.fixed_data import url

user = user()
passw = passw()

class TestRegistration:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(url + 'user/register')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        self.driver.quit()

    def test_registration(self, setup):
        filling_text(self.driver, "css", "input[placeholder='Username']", user['username'])
        filling_text(self.driver, "css", "input[placeholder='Email']", user['email'])
        filling_text(self.driver, "css", "input[placeholder='Password']", passw)
        click_element(self.driver, "xpath", "//button[contains(text(), 'Sign up')]")
        edit = get_elements(self.driver, "class", "ion-compose")[0]
        WebDriverWait(self.driver, 10).until(EC.visibility_of(edit))
        assert self.driver.current_url == "https://conduit.mate.academy/"
        assert user['username'] == get_elements(self.driver, 'css', 'li.nav-item a.nav-link')[3].text
        assert EC.visibility_of(edit)
        assert ' Settings' == get_elements(self.driver, 'css', 'li.nav-item a.nav-link')[2].text