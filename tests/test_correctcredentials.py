import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # For automatic ChromeDriver setup
import os  # For handling environment variables

class TestCorrectcredentials:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Use webdriver-manager to automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_correctcredentials(self):
        print(" Opening login page...")
        self.driver.get("http://web:8000/auth/login/")  # Ensure the correct URL is used
        self.driver.set_window_size(1050, 652)

        print("Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin")  # Using hardcoded credentials for testing

        print(" Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("admin1")  # Using hardcoded credentials for testing

        print(" Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-login")
        login_button.click()

        print(" Waiting for Dashboard to appear...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print(" Successfully logged in. Dashboard is visible.")
        except Exception as e:
            print(" Login might have failed. Dashboard element not found.")
            raise e

        # Assert URL contains dashboard or home
        current_url = self.driver.current_url.lower()
        print(f" Redirected to: {current_url}")
        assert "dashboard" in current_url or "home" in current_url, \
            f" Login did not redirect to dashboard/home. URL: {current_url}"