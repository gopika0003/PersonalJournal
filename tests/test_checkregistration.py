import pytest
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
        chrome_options.add_argument("--headless")  # Headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_checkregistration(self):
        print("🔎 Opening login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print("🔗 Clicking on 'Sign Up' link...")
        sign_up_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sign Up")))
        sign_up_link.click()

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("user1")

        print("🧪 Entering email...")
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("user@gmail.com")

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("user12")

        print("🚀 Clicking register button...")
        register_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-register")
        register_button.click()

        print("⏳ Waiting for dashboard redirection...")
        self.wait.until(EC.url_contains("/journal/dashboard/"))

        current_url = self.driver.current_url
        print(f"🌐 Redirected to: {current_url}")

        assert "/journal/dashboard/" in current_url, \
            f"❌ Registration did not redirect to dashboard. Current URL: {current_url}"
        print("✅ Registration redirected to dashboard successfully.")
