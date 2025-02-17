from dataclasses import dataclass
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

options = Options()

options.add_argument("--headless")
options.add_argument("--disable-gpu")


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")

COMPUTERS_URL = urljoin(HOME_URL, "computers/")
LAPTOPS_URL = urljoin(COMPUTERS_URL, "laptops/")
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
    rating = int(product.find_element(By.CSS_SELECTOR, "p[data-rating]").get_attribute("data-rating"))
    num_of_reviews = int(product.find_element(By.CLASS_NAME, "review-count").text.split(" ")[0])

    product = Product(
        title=title,
        description=description,
        price=price,
        rating=rating,
        num_of_reviews=num_of_reviews
    )

    return product


def get_page_products(link: str) -> list[Product]:
    with webdriver.Chrome(options=options) as driver:
        driver.get(link)
        web_product = driver.find_element(By.CLASS_NAME, "card")
        product = get_single_product(web_product)
        print(product)


def get_all_products(links: list) -> None:
    for link in links:
        file_name = f"{link.split('/')[-2]}.csv"

        page_products = get_page_products(link)

        with open(file_name, "w", encoding="utf-8") as f:
            pass


if __name__ == "__main__":
    all_links = [
        HOME_URL, COMPUTERS_URL, LAPTOPS_URL, TABLETS_URL, PHONES_URL, TOUCH_PHONES_URL
    ]
    get_all_products(all_links)
