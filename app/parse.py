import csv
import time
from dataclasses import dataclass, fields, astuple
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

options = Options()

options.add_argument("--headless")
options.add_argument("--disable-gpu")


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")

COMPUTERS_URL = urljoin(HOME_URL, "computers/")
LAPTOPS_URL = urljoin(COMPUTERS_URL, "laptops")
TABLETS_URL = urljoin(COMPUTERS_URL, "tablets/")

PHONES_URL = urljoin(HOME_URL, "phones/")
TOUCH_PHONES_URL = urljoin(PHONES_URL, "touch/")


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def get_single_product(product: WebElement) -> Product:
    title = product.find_element(By.CLASS_NAME, "title").get_attribute("title")
    description = product.find_element(By.CLASS_NAME, "description").text
    price = float(product.find_element(By.CLASS_NAME, "price").text.replace("$", ""))
    rating = len(product.find_elements(By.CLASS_NAME, "ws-icon-star"))
    num_of_reviews = int(product.find_element(By.CLASS_NAME, "review-count").text.split(" ")[0])
    # TO DO: write a function to get attribute name of element with try/except block

    product = Product(
        title=title,
        description=description,
        price=price,
        rating=rating,
        num_of_reviews=num_of_reviews
    )

    return product


def get_page_products(link: str, start: int = 1) -> List[Product]:
    with webdriver.Chrome(options=options) as driver:
        driver.get(link)

        try:
            driver.find_element(By.ID, "closeCookieBanner").click()
            print("Click on cookie banner.")
        except NoSuchElementException:
            pass

        more = True

        page_products = []

        while more is not None:
            first_xpath = f"/html/body/div[1]/div[3]/div/div[2]/div/div[{start}]"
            print(start)

            try:
                web_product = driver.find_element(By.XPATH, first_xpath)
                product = get_single_product(web_product)
                print(product)
                page_products.append(product)
            except NoSuchElementException:
                print("That was the last product, try to click 'more'.")
                time.sleep(2.0)
                try:
                    more = driver.find_element(
                        By.CLASS_NAME, "ecomerce-items-scroll-more"
                    )
                except NoSuchElementException as e:
                    more = None
                    print("There are not 'more'.")
                else:
                    print("Try to get more products.")
                    try:
                        more.click()
                        print("Get more products")
                    except ElementNotInteractableException as e:
                        print("Can't click on MORE")
                        break
            else:
                start += 1

        return page_products


def get_all_products(links: list) -> None:
    for link in links:
        print(link)
        print("https://webscraper.io/test-sites/e-commerce/more/computers/laptops/")
        file_name = f"{link.split('/')[-2]}.csv"

        page_products = get_page_products(link)

        with open(file_name, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([field.name for field in fields(Product)])
            writer.writerows([astuple(product) for product in page_products])


if __name__ == "__main__":
    # all_links = [
    #     HOME_URL, COMPUTERS_URL, LAPTOPS_URL, TABLETS_URL, PHONES_URL, TOUCH_PHONES_URL
    # ]
    all_links = [LAPTOPS_URL]
    get_all_products(all_links)
