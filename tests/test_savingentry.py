import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

class TestSavingEntry:
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

    def test_savingentry(self):
        print("🔎 Opening login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin1")

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("admin1")

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-login")
        login_button.click()

        print("⏳ Waiting for dashboard to load...")
        try:
            dashboard_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome to your personal journal')]"))
            )
            print("✅ Dashboard loaded successfully.")
        except Exception as e:
            print("❌ Dashboard did not load. Login might have failed.")
            self.driver.save_screenshot("login_failed.png")
            print("🔗 Current URL after login:", self.driver.current_url)
            raise e

        print("🔗 Navigating to 'New Entry' page...")
        try:
            new_entry_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "📝 New Entry")))
            new_entry_link.click()
        except Exception as e:
            print("❌ 'New Entry' link not found.")
            self.driver.save_screenshot("new_entry_failed.png")
            raise e

        print("📝 Filling out the entry form...")
        try:
            title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
            title_input.send_keys("A good day!")

            content_input = self.driver.find_element(By.ID, "content")
            content_input.send_keys("Today it was a good day.")
        except Exception as e:
            print("❌ Failed to fill out the entry form.")
            self.driver.save_screenshot("form_fill_failed.png")
            raise e

        print("🚀 Submitting the entry...")
        try:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-submit")
            submit_button.click()
        except Exception as e:
            print("❌ Failed to submit the entry.")
            self.driver.save_screenshot("entry_submit_failed.png")
            raise e

        print("⏳ Waiting for confirmation message...")
        try:
            confirmation_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Entry saved successfully')]"))
            )
            print(f"✅ Entry saved successfully: {confirmation_message.text}")
        except Exception as e:
            print("❌ Entry might not have been saved. Confirmation message not found.")
            self.driver.save_screenshot("entry_confirmation_failed.png")
            raise e

        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "entries" in current_url or "dashboard" in current_url, \
            f"❌ Entry save did not redirect to entries or dashboard. URL: {current_url}"
