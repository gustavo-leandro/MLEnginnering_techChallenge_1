"""
Scraping functions to collect book data from books.toscrape.com.
Target table: tb_books
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import re
from .schemas import BookCreate

BASE_URL: str = "https://books.toscrape.com/catalogue/page-{}.html"


def scrape_books(pages: int = 50) -> List[BookCreate]:
    """
    Scrapes books from books.toscrape.com, collecting all relevant information.
    Args:
            pages (int): Number of pages to collect (default=50)
    Returns:
            List[BookCreate]: List of extracted book data
    """
    books = []
    base_site = "https://books.toscrape.com/catalogue/"

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        resp = requests.get(url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        ls_articles = soup.find_all("article", class_="product_pod")
        ls_links = [link.h3.a["href"] for link in ls_articles]

        for link in ls_links:
            book_resp = requests.get(base_site + link)
            book_resp.raise_for_status()
            book_soup = BeautifulSoup(book_resp.text, "html.parser")

            # Extract book attributes
            b_title = book_soup.find("h1").get_text(strip=True)

            breadcrumbs = book_soup.find("ul", class_="breadcrumb").find_all("li")
            b_category = breadcrumbs[-2].get_text(strip=True)

            class_rating = book_soup.find("p", class_="star-rating")["class"]
            ratings_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            b_rating = ratings_dict[class_rating[1]]

            desc_header = book_soup.find("div", id="product_description")
            if desc_header:
                desc_p = desc_header.find_next_sibling("p")
                b_description = desc_p.get_text(strip=True) if desc_p else ""
            else:
                b_description = ""

            img_tag = book_soup.find("div", class_="item active").img
            b_img_src = "https://books.toscrape.com/" + img_tag["src"]

            info_table = book_soup.find("table", class_="table table-striped")
            for row in info_table.find_all("tr"):
                if row.th.get_text(strip=True) == "UPC":
                    b_upc = row.td.get_text(strip=True)
                elif row.th.get_text(strip=True) == "Product Type":
                    b_product_type = row.td.get_text(strip=True)
                elif row.th.get_text(strip=True) == "Price (excl. tax)":
                    b_price_excl_tax = float(
                        re.sub(r"[^0-9.]", "", row.td.get_text(strip=True))
                    )
                elif row.th.get_text(strip=True) == "Price (incl. tax)":
                    b_price_incl_tax = float(
                        re.sub(r"[^0-9.]", "", row.td.get_text(strip=True))
                    )
                elif row.th.get_text(strip=True) == "Tax":
                    b_tax = float(re.sub(r"[^0-9.]", "", row.td.get_text(strip=True)))
                elif row.th.get_text(strip=True) == "Availability":
                    availability_text = row.td.get_text(strip=True)
                    b_num_available = (
                        int(re.search(r"\d+", availability_text).group())
                        if re.search(r"\d+", availability_text)
                        else 0
                    )
                elif row.th.get_text(strip=True) == "Number of reviews":
                    b_num_reviews = int(row.td.get_text(strip=True))

            books.append(
                BookCreate(
                    title=b_title,
                    category=b_category,
                    rating=b_rating,
                    description=b_description,
                    image_url=b_img_src,
                    upc=b_upc,
                    product_type=b_product_type,
                    price_excl_tax=b_price_excl_tax,
                    price_incl_tax=b_price_incl_tax,
                    tax=b_tax,
                    num_available=b_num_available,
                    num_reviews=b_num_reviews,
                )
            )

    return books
