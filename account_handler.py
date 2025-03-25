import logging
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class AccountHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup_webdriver(self):
        options = Options()
        options.add_argument("--start-maximized")
        service = Service(executable_path="chromedriver.exe")  # your chromedriver path
        return webdriver.Chrome(service=service, options=options)

    def generate_name(self):
        first_names = ["Adi"]
        last_names = ["Santoso"]
        return random.choice(first_names), random.choice(last_names)

    def generate_username(self, first_name, last_name):
        random_number = random.randint(100, 999)
        random_string = "".join(random.choices(string.ascii_lowercase, k=3))
        return f"{first_name.lower()}{last_name.lower()}{random_number}{random_string}"

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    def wait_for_username_error(self, driver):
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@aria-live='assertive']//div[contains(text(), 'That username is taken. Try another.')]",
                    )
                )
            )
            return error_message.is_displayed()
        except Exception:
            return False

    def handle_username(self, driver, username):
        username_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label='Username']")
            )
        )
        username_input.clear()
        username_input.send_keys(username)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
        )
        next_button.click()

    def create_account(self, first_name, last_name, username, password):
        driver = self.setup_webdriver()
        try:
            driver.get("https://accounts.google.com/signup")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "firstName"))
            ).send_keys(first_name)
            driver.find_element(By.ID, "lastName").send_keys(last_name)

            month_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "month"))
            )
            Select(month_field).select_by_index(random.randint(1, 12))

            day_field = driver.find_element(By.ID, "day")
            day_field.send_keys(str(random.randint(1, 28)))

            year_field = driver.find_element(By.ID, "year")
            year_field.send_keys(str(random.randint(1980, 2005)))

            gender_field = driver.find_element(By.ID, "gender")
            Select(gender_field).select_by_index(random.randint(1, 3))

            self.handle_username(driver, username)
            while self.wait_for_username_error(driver):
                username = self.generate_username(first_name, last_name)
                self.handle_username(driver, username)

            password_field = driver.find_element(
                By.CSS_SELECTOR, "input[aria-label='Password']"
            )
            password_field.send_keys(password)
            confirm_password_field = driver.find_element(
                By.CSS_SELECTOR, "input[aria-label='Confirm']"
            )
            confirm_password_field.send_keys(password)

        except Exception as e:
            self.logger.error(f"Error creating account: {e}")
        finally:
            driver.quit()
