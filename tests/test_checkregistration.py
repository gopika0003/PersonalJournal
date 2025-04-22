import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestCheckRegistration:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_check_registration(self):
        print(" Opening login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print(" Clicking 'Sign Up' link...")
        signup_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
        signup_link.click()

        print("Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_NEW_USERNAME", "newuser"))

        print(" Entering email...")
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys(os.getenv("TEST_NEW_EMAIL", "newuser@gmail.com"))

        print(" Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_NEW_PASSWORD", "newuser1"))

        print(" Clicking 'Register' button...")
        register_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-register")
        register_button.click()

        print(" Waiting for dashboard or confirmation page...")
        try:
            confirmation_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print(" Successfully registered and redirected.")
        except Exception as e:
            print(" Registration failed or confirmation page not loaded.")
            raise e

        assert confirmation_element is not None, "Confirmation element not found. Registration might have failed."
        print(" Registration test passed.")
