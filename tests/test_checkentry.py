import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestCheckEntry:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: remove if you want browser to open
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_checkentry(self):
        print("🔐 Logging in...")
        self.driver.get("http://localhost:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_EXISTING_USERNAME", "admin"))

        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_EXISTING_PASSWORD", "admin1"))

        self.driver.find_element(By.CSS_SELECTOR, ".btn-login").click()

        print("📝 Navigating to New Entry...")
        new_entry_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "📝 New Entry")))
        new_entry_link.click()

        print("📓 Filling out the entry form...")
        self.wait.until(EC.presence_of_element_located((By.ID, "title"))).send_keys("a happy day")
        self.driver.find_element(By.ID, "content").send_keys("today it was a wonderful day.")

        print("🚀 Submitting the entry...")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()

        print("✅ Checking for success message...")
        success_message = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Saved successfully')]"))
        )

        assert success_message is not None, "❌ Entry not saved successfully."
        print("🎉 Entry saved successfully.")
