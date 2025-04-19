import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # For automatic ChromeDriver setup
import os  # For handling environment variables

class TestIncorrectcredentials:
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

    def test_incorrectcredentials(self):
        print("🔎 Opening login page...")
        self.driver.get("http://web:8000/auth/login/")  # Ensure the correct URL is used
        self.driver.set_window_size(1050, 652)

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("abc")  # Using incorrect credentials for testing

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("fghj")  # Using incorrect credentials for testing

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-login")
        login_button.click()

        print("⏳ Waiting for error message to appear...")
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            print(f"✅ Error message displayed: {error_message.text}")
        except Exception as e:
            print("❌ Error message not found. Login might have succeeded unexpectedly.")
            raise e

        # Assert that the error message contains "invalid"
        error_text = error_message.text.lower()
        assert "invalid" in error_text, f"❌ Error message does not indicate invalid credentials. Found: {error_text}"