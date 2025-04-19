import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

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

        # Either check for success message or redirection to login
        print("⏳ Waiting for success message or login redirection...")

        redirected = False
        success_text_found = False

        try:
            # Try to detect success message (optional)
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            if "account created" in success_message.text.lower():
                success_text_found = True
                print(f"✅ Success message found: {success_message.text}")
        except:
            print("⚠️ Success message not found, checking for URL redirection...")

        # Now check the current URL
        current_url = self.driver.current_url.lower()
        print(f"🌐 Current URL: {current_url}")

        if "login" in current_url:
            redirected = True
            print("✅ Registration redirected to login page.")

        # Final assertion
        assert redirected or success_text_found, \
            "❌ Neither success message nor redirection to login page detected."
