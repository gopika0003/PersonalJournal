import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # For automatic ChromeDriver setup

class TestSaveentry:
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

    def test_saveentry(self):
        print("🔎 Opening login page...")
        self.driver.get("http://web:8000/auth/login//")  # Ensure the correct URL is used
        self.driver.set_window_size(1050, 652)

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin")  # Using hardcoded credentials for testing

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("admin1")  # Using hardcoded credentials for testing

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn")
        login_button.click()

        print("🔗 Navigating to 'New Entry' page...")
        new_entry_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "📝 New Entry")))
        new_entry_link.click()

        print("📝 Filling out the entry form...")
        title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        title_input.send_keys("good day")

        content_input = self.driver.find_element(By.ID, "content")
        content_input.send_keys("today it was a happy day.")

        print("🚀 Submitting the entry...")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-submit")
        submit_button.click()

        print("⏳ Waiting for confirmation message...")
        try:
            confirmation_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Entry saved successfully')]"))
            )
            print(f"✅ Entry saved successfully: {confirmation_message.text}")
        except Exception as e:
            print("❌ Entry might not have been saved. Confirmation message not found.")
            raise e

        # Assert that the user is redirected to the entries list or dashboard
        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "entries" in current_url or "dashboard" in current_url, \
            f"❌ Entry save did not redirect to entries or dashboard. URL: {current_url}"
