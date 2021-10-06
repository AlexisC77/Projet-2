import requests
import csv
from bs4 import BeautifulSoup
homePageUrl = "https://books.toscrape.com/catalogue/page-1.html"


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


def main(homeUrl):
    homePage = requests.get(homeUrl)
    soupHome = BeautifulSoup(homePage.content, "html.parser")
    categoryList = soupHome.find("div", class_="side_categories").find_all("a")
    categoriesForUrl = []
    categories = []
    number = 1
    for i in categoryList:
        category = i.string.strip() + "_" + str(number)
        category = category.replace(" ", "-").lower()
        categoriesForUrl.append(category)
        categories.append(i.string.strip())
        number += 1
    print(categoriesForUrl)
    print(categories)
    booksUrlList = []
    number = 1
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]
    with open('product.csv', "w", newline="") as file_csv:
        writer = csv.writer(file_csv, delimiter=",")
        writer.writerow(en_tete)
    for i in categoriesForUrl[1:]:
        url = "https://books.toscrape.com/catalogue/category/books/"+i+"/index.html"
        getBooksUrl(url, booksUrlList, i)
        for y in booksUrlList:
            book = product(y, categories[number])
            with open('product.csv', "a", newline="") as file_csv:
                writer = csv.writer(file_csv, delimiter=",")
                writer.writerow([book.product_page_url, book.universal_product_code, book.title, book.price_including_tax, book.price_excluding_tax, book.number_available, book.product_description, book.category, book.review_rating, book.image_url])
        booksUrlList = []
        number += 1


def product(url, category):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find_all("div", class_=False)
    title = soup.find("h1").string
    productInformation = soup.find_all("td")
    productUrl = url
    upc = productInformation[0].string
    priceIncludingTax = productInformation[3].string
    priceExcludingTax = productInformation[2].string
    availability = productInformation[5].string
    reviewRating = soup.find("p", class_="star-rating")["class"][1]
    if reviewRating == "One":
        reviewRating = 1
    elif reviewRating == "Two":
        reviewRating = 2
    elif reviewRating == "Three":
        reviewRating = 3
    elif reviewRating == "Four":
        reviewRating = 4
    else:
        reviewRating = 5
    print(reviewRating)
    imageUrl = soup.find("img")
    print("upc = " + upc)
    print("title = " + title)
    print("price excluding taxes =" + priceExcludingTax)
    print("price Including taxes =" + priceIncludingTax)
    if availability[:8] == "In stock":
        numberAvailable = availability[10:-11]
    else:
        numberAvailable = 0
    print(numberAvailable)
    print("url of this product is:" + productUrl)
    print(category)
    # print(description)
    # print(imageUrl)
    # print(imageUrl.string)
    # print(type(imageUrl))
    # print(imageUrl.get('href'))
    # print(description[3].contents)
    book = Book(url, upc, title, priceExcludingTax, priceIncludingTax, numberAvailable, "description", category, reviewRating, "imageUrl")
    return book


def getBooksUrl(url, booksUrlList, category):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    booksUrl = []
    next = "next" == soup.find_all("a")[-1].string
    previous = "previous" == soup.find_all("a")[-2].string or "previous" == soup.find_all("a")[-1].string
    for a in soup.find_all("a"):
        booksUrl.append(a["href"])
    del booksUrl[0:54]
    if next:
        partUrlNext = booksUrl[-1]
        del booksUrl[-1]
    if previous:
        del booksUrl[-1]
    for i in booksUrl:
        i = i.replace("../../../", "")
        if "https://books.toscrape.com/catalogue/"+i not in booksUrlList:
            booksUrlList.append("https://books.toscrape.com/catalogue/"+i)
    if next:
        urlNext = "https://books.toscrape.com/catalogue/category/books/" + category + "/" + partUrlNext
        getBooksUrl(urlNext, booksUrlList, category)


main(homePageUrl)
# product("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", "travel")
test = Book("product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url")

