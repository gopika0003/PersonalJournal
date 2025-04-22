import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestIncorrectcredentials:
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

    def test_incorrectcredentials(self):
        print(" Opening login page...")
        self.driver.get("http://web:8000/auth/login/")
        self.driver.set_window_size(1050, 652)

        print(" Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("abc")

        print(" Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("fghj")

        print(" Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-login")
        login_button.click()

        print(" Waiting for error message to appear...")
        error_message = None

        try:
            # Try primary selector first
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
        except Exception as e:
            print(" '.alert-danger' not found. Trying fallback selector...")
            # Fallback to any 'alert' class (more generic)
            try:
                error_message = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert"))
                )
            except Exception as ex:
                # Print the page source to help debug what's actually rendered
                print(" Full page HTML after login attempt:")
                print(self.driver.page_source)
                print(" No error message found using fallback selectors.")
                raise ex

        # Check and assert the message text
        assert error_message is not None, " Error message element not found."
        error_text = error_message.text.strip().lower()
        print(f" Error message displayed: {error_text}")
        assert "invalid" in error_text or "incorrect" in error_text, \
            f" Error message does not indicate login failure. Found: '{error_text}'"
