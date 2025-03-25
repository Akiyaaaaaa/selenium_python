import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class ReviewHandler:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def write_review(self, place_name, review_text):
        try:
            self.driver.get("https://maps.google.com")
            search_field = self.driver.find_element(
                By.XPATH, '//*[@id="searchboxinput"]'
            )
            search_field.send_keys(place_name)
            self.driver.find_element(
                By.XPATH, '//*[@id="searchbox-searchbutton"]'
            ).click()

            review_button = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//button[contains(@aria-label, "Write a review")]')
                )
            )
            review_button.click()

            star_rating = self.driver.find_element(By.XPATH, "//div[@data-rating='5']")
            star_rating.click()

            review_field = self.driver.find_element(
                By.XPATH, '//textarea[@aria-label="Enter review"]'
            )
            review_field.send_keys(review_text)

            submit_button = self.driver.find_element(
                By.XPATH, '//button[@data-action="submit"]'
            )
            submit_button.click()
            self.logger.info("Review submitted successfully.")
        except NoSuchElementException as e:
            self.logger.error(f"Error writing review: {e}")
