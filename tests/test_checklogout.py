import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestLogout:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def teardown_method(self, method):
        self.driver.quit()

    def test_logout(self):
        print("🔐 Navigating to login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print("👤 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin")

        print("🔑 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("admin1")

        print("➡️ Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn")
        login_button.click()

        print("📄 Waiting for dashboard to load...")
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))

        print("🚪 Clicking logout...")
        logout_link = self.driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()

        print("🔄 Verifying redirect to login page...")
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))

        current_url = self.driver.current_url
        print(f"✅ Successfully redirected to login page: {current_url}")
        assert "login" in current_url.lower(), f"❌ Expected to be on login page, got: {current_url}"
