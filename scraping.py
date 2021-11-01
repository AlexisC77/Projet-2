# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup
import os
home_page_url = "https://books.toscrape.com/catalogue/page-1.html"
# change the value of "restart_value" by the number of the next category to restart It from this point, It is given by the script, his normal value is 1
restart_value = 1


class Book:
    def __init__(self, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
        self.product_page_url = product_page_url
        self.universal_product_code = universal_product_code
        self.title = title
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url


def main(home_url):
    print("code is running")
    home_page = requests.get(home_url)
    soup_home = BeautifulSoup(home_page.content, "html.parser")
    category_list = soup_home.find("div", class_="side_categories").find_all("a")
    categories_for_url = []
    categories = []
    number_category = 1
    for category in category_list:
        category_url = category.string.strip() + "_" + str(number_category)
        category_url = category_url.replace(" ", "-").lower()
        categories_for_url.append(category_url)
        categories.append(category.string.strip())
        number_category += 1
    books_url_list = []
    categories_number = number_category
    number_category = restart_value
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]
    for category in categories_for_url[number_category:]:
        if not os.path.isdir(categories[number_category]):
            os.mkdir(categories[number_category])
        os.chdir(categories[number_category])
        with open(categories[number_category]+".csv", "w", newline="") as file_csv:
            writer = csv.writer(file_csv, delimiter=",")
            writer.writerow(en_tete)
        url = "https://books.toscrape.com/catalogue/category/books/"+category+"/index.html"
        get_books_url(url, books_url_list, category, categories_number)
        for books_url in books_url_list:
            book = product(books_url, categories[number_category])
            download_picture(book.image_url, book.title)
            with open(categories[number_category]+".csv", "a", newline="", encoding='utf-8') as file_csv:
                writer = csv.writer(file_csv, delimiter=",")
                writer.writerow([book.product_page_url, book.universal_product_code, book.title, book.price_including_tax, book.price_excluding_tax, book.number_available, book.product_description, book.category, book.review_rating, book.image_url])
        books_url_list = []
        os.chdir("..")
        print(categories[number_category]+" is done")
        number_category += 1
        print("the number of the next category is :"+str(number_category))
    print("program is done you can now look at .csv")


def product(url, category):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("h1").string
    product_information = soup.find_all("td")
    upc = product_information[0].string
    price_including_tax = product_information[3].string
    price_excluding_tax = product_information[2].string
    availability = product_information[5].string
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    if review_rating == "One":
        review_rating = 1
    elif review_rating == "Two":
        review_rating = 2
    elif review_rating == "Three":
        review_rating = 3
    elif review_rating == "Four":
        review_rating = 4
    else:
        review_rating = 5
    image_url = "https://books.toscrape.com/"+soup.find("img")["src"].replace("../../", "")
    if availability[:8] == "In stock":
        number_available = availability[10:-11]
    else:
        number_available = 0
    description = soup.find_all("meta")[2]["content"].strip()
    book = Book(url, upc, title, price_excluding_tax, price_including_tax, number_available, description, category, review_rating, image_url)
    return book


def get_books_url(url, books_url_list, category, categories_number):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    books_url = []
    next = "next" == soup.find_all("a")[-1].string
    previous = "previous" == soup.find_all("a")[-2].string or "previous" == soup.find_all("a")[-1].string
    for a in soup.find_all("a"):
        books_url.append(a["href"])
    del books_url[0:categories_number+2]
    if next:
        part_url_next = books_url[-1]
        del books_url[-1]
    if previous:
        del books_url[-1]
    for i in books_url:
        i = i.replace("../../../", "")
        if "https://books.toscrape.com/catalogue/"+i not in books_url_list:
            books_url_list.append("https://books.toscrape.com/catalogue/"+i)
    if next:
        url_next = "https://books.toscrape.com/catalogue/category/books/" + category + "/" + part_url_next
        get_books_url(url_next, books_url_list, category, categories_number)


def download_picture(url, title):
    title = title.replace(":", ";").replace("/", "").replace("\"", "").replace("\\", "").replace("*", "").replace("?", "").replace("’", "")
    response = requests.get(url).content
    with open(title+".jpg", "wb") as picture:
        picture.write(response)


main(home_page_url)
