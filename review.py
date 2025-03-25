import logging
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Lists of common Indonesian names
first_names = [
    "Adi",
    # "Budi",
    # "Cahya",
    # "Dewi",
    # "Eka",
    # "Fajar",
    # "Gita",
    # "Hari",
    # "Indah",
    # "Joko",
    # "Kirana",
    # "Lestari",
    # "Made",
    # "Nur",
    # "Putri",
    # "Rina",
    # "Sari",
    # "Taufik",
    # "Utami",
    # "Wayan",
]
last_names = [
    "Santoso",
    # "Wijaya",
    # "Pratama",
    # "Putra",
    # "Sukma",
    # "Hadi",
    # "Sutrisno",
    # "Kurniawan",
    # "Saputra",
    # "Rahman",
    # "Pangestu",
    # "Cahyadi",
    # "Iskandar",
    # "Hartono",
    # "Wibowo",
    # "Nugroho",
    # "Firmansyah",
    # "Suryadi",
    # "Hakim",
    # "Syahputra",
]


def generate_name():
    """Generate a realistic Indonesian name."""
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name


def generate_username(first_name, last_name):
    """Generate a unique username."""
    random_number = random.randint(100, 999)
    random_string = "".join(random.choices(string.ascii_lowercase, k=3))
    username = f"{first_name.lower()}{last_name.lower()}{random_number}{random_string}"
    return username


def generate_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def setup_webdriver():
    """Set up the Selenium WebDriver."""
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(
        executable_path="chromedriver.exe"
    )  # Update path to your ChromeDriver
    return webdriver.Chrome(service=service, options=options)


def wait_for_username_error(driver):
    """Waits for the username error message to disappear."""
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@aria-live='assertive']//div[contains(text(), 'That username is taken. Try another.')]",
                )
            )
        )
        logging.info(error_message.is_displayed())
        if error_message.is_displayed():
            logging.info("Username is taken. Please try another.")
            return True  # Error message is displayed
    except Exception as e:
        logging.info(f"No username error found. error : {e}")
    return False  # Error message is not found or disappeared


def write_review(driver, place_name, review_text):
    """Write a review on Google Maps."""
    try:
        # Navigate to Google Maps
        driver.get("https://maps.google.com")

        # Search for the location
        search_field = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        search_field.send_keys(place_name)
        driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
        time.sleep(5)  # Adjust this to ensure the location is loaded

        # Click review button
        review_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[contains(@aria-label, "Tulis ulasan")]')
            )
        )
        review_button.click()
        time.sleep(2)

        # Rate 4 or 5 stars
        random_number = random.randint(1, 2)
        if random_number == 1:
            star_rating = driver.find_element(By.XPATH, "//div[@data-rating='4']")
            star_rating.click()
        else:
            star_rating = driver.find_element(By.XPATH, "//div[@data-rating='5']")
            star_rating.click()

        # Enter review text
        review_field = driver.find_element(
            By.XPATH, '//textarea[@aria-label="Enter review"]'
        )
        review_field.send_keys(review_text)

        # Submit the review
        submit_button = driver.find_element(By.XPATH, '//button[@data-action="submit"]')
        submit_button.click()
        logging.info("Review submitted successfully.")
        time.sleep(5)
    except NoSuchElementException as e:
        logging.error(f"Error while writing review: {e}")


def handle_username(driver, username):
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
    return


def create_gmail_account(
    first_name, last_name, username, password, place_name, review_text
):
    """Automate Gmail account creation and write a review."""
    logging.info("Starting Gmail account creation process.")
    driver = setup_webdriver()

    try:
        # Navigate to Gmail sign-up page
        driver.get("https://accounts.google.com/signup")
        time.sleep(2)  # Wait for the page to load

        # Fill out the sign-up form
        driver.find_element(By.ID, "firstName").send_keys(first_name)
        driver.find_element(By.ID, "lastName").send_keys(last_name)
        driver.find_element(By.XPATH, "//button[.//span[text()='Next']]").click()

        # Fill birthdate and gender
        # Wait for the 'month' dropdown to be present
        month_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        Select(month_field).select_by_index(random.randint(1, 12))

        # Wait for the 'day' field and input a random day
        day_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "day"))
        )
        day_field.clear()
        day_field.send_keys(str(random.randint(1, 28)))

        # Wait for the 'year' field and input a random year
        year_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "year"))
        )
        year_field.clear()
        year_field.send_keys(str(random.randint(1980, 2005)))

        # Wait for the 'gender' dropdown to be present
        gender_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gender"))
        )
        Select(gender_field).select_by_index(random.randint(1, 3))

        logging.info("Birthdate and gender fields filled successfully.")

        # Wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
        )
        next_button.click()

        # Retry username if it's already taken
        while True:
            handle_username(driver, username)
            logging.info("Username field filled successfully.")

            if wait_for_username_error(driver):
                logging.error(
                    f"Username '{username}' is already taken, retrying with a new username."
                )
                username = generate_username(first_name, last_name)
                logging.info(f"Generated new username: {username}")
            else:
                logging.info(f"Username '{username}' is available.")
                break  # Exit the loop if username is valid

        # driver.find_element(By.ID, "username").send_keys(username)
        # driver.find_element(By.XPATH, "//button[.//span[text()='Next']]").click()

        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label='Password']")
            )
        )
        password_field.send_keys(password)

        confirm_password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label='Confirm']")
            )
        )
        confirm_password_field.send_keys(password)
        # driver.find_element(By.NAME, "Passwd").send_keys(password)
        # driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)

        # Submit the form
        logging.info(f"Account creation attempted for username: {username}.")
        time.sleep(5)

        # Write a review
        write_review(driver, place_name, review_text)
    except NoSuchElementException as e:
        logging.error(f"Element not found: {e}")
    except TimeoutException as e:
        logging.error(f"Timeout occurred: {e}")
    finally:
        driver.quit()


def main():
    """Main function to demonstrate the script."""
    # Generate review texts
    review_texts = [
        "Beautiful location with stunning views of the Andes mountains.",
        "Exceptional service from friendly and helpful staff.",
        "Comfortable and spacious rooms, great for a relaxing stay.",
        "Convenient location, easy access to local attractions.",
        "Impressive wine selection, perfect for wine lovers.",
        "Great value for money, offering excellent amenities.",
        "Clean and well-maintained facilities, ensuring a pleasant stay.",
        "Wide range of activities available, great for adventurous travelers.",
    ]

    # Number of reviews to create
    num_reviews = 1

    # Place name
    place_name = "Java Sea"

    for i in range(num_reviews):
        # Generate names, usernames, and passwords
        first_name, last_name = generate_name()
        username = generate_username(first_name, last_name)
        password = generate_password()
        logging.info(f"Generated name: {first_name} {last_name}")
        logging.info(f"Generated username: {username}")
        logging.info(f"Generated password: {password}")

        # Step 1: Create a Gmail account (for educational purposes, no CAPTCHA handling)
        create_gmail_account(
            first_name,
            last_name,
            username,
            password,
            place_name,
            [review_texts[i % len(review_texts)]],
        )


if __name__ == "__main__":
    main()
