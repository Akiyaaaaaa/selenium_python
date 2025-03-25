import logging
from account_handler import AccountHandler
from review_handler import ReviewHandler


def main():
    logging.basicConfig(level=logging.INFO)
    account_handler = AccountHandler()
    first_name, last_name = account_handler.generate_name()
    username = account_handler.generate_username(first_name, last_name)
    password = account_handler.generate_password()

    account_handler.create_account(first_name, last_name, username, password)

    driver = account_handler.setup_webdriver()
    try:
        review_handler = ReviewHandler(driver)
        review_handler.write_review("Java Sea", "Amazing place with beautiful scenery!")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
