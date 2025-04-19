import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCheckEntry:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def test_checkentry(self):
        print("🔐 Logging in...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        # Logging in with credentials
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_EXISTING_USERNAME", "admin"))

        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_EXISTING_PASSWORD", "admin1"))

        self.driver.find_element(By.CSS_SELECTOR, ".btn-login").click()

        print("📝 Navigating to New Entry...")
        new_entry_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-new-entry")))
        new_entry_button.click()

        print("📓 Filling out the entry form...")
        self.wait.until(EC.presence_of_element_located((By.ID, "title"))).send_keys("A happy day")
        content_input = self.driver.find_element(By.ID, "content")
        content_input.send_keys("Today it was a wonderful day.")

        print("🚀 Submitting the entry...")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()

        print("⏳ Waiting for the success message...")
        success_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))

        assert "Saved successfully!" in success_message.text

    def teardown_method(self):
        time.sleep(2)  # Giving it some time to verify the result before closing the browser
        self.driver.quit()
