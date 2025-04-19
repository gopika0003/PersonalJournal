import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestViewEntries:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Comment out if you want to see the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def teardown_method(self, method):
        self.driver.quit()

    def test_viewentries(self):
        print("🔐 Opening login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print("🧪 Entering credentials...")
        username = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys("admin")
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys("admin1")

        print("🚀 Logging in...")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        print("📂 Clicking on 'View Entries'...")
        view_entries_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📜 View Entries"))
        )
        view_entries_link.click()

        print("⏳ Waiting for entries to load...")
        entries_loaded = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "entry"))
        )

        assert entries_loaded is not None, "❌ No entries found!"
        print("✅ Entries displayed successfully.")
