import requests
from bs4 import BeautifulSoup
homePageUrl = "https://books.toscrape.com/catalogue/page-1.html"


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
    for i in categoriesForUrl[1:]:
        url = "https://books.toscrape.com/catalogue/category/books/"+i+"/index.html"
        getBooksUrl(url, booksUrlList, i)
        for y in booksUrlList:
            product(y, categories[number])
        booksUrlList = []
        number += 1


def product(url, category):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # description = soup.find_all("div", class_=False)
    title = soup.find("h1").string
    productInformation = soup.find_all("td")
    productUrl = url
    upc = productInformation[0].string
    priceIncludingTax = productInformation[3].string
    priceExcludingTax = productInformation[2].string
    availability = productInformation[5].string
    reviewNumber = productInformation[6].string
    reviewRating = soup.find("p", class_="star-rating")["class"][1]
    # if reviewRating == "One":
    #     reviewRating = 1
    # elif reviewRating == "Two":
    #     reviewRating = 2
    # elif reviewRating == "Three":
    #     reviewRating = 3
    # elif reviewRating == "Four":
    #     reviewRating = 4
    # else:
    #     reviewRating = 5
    # print(reviewRating)
    # imageUrl = soup.find("img")
    # print("upc = " + upc)
    # print("title = " + title)
    # print("price excluding taxes =" + priceExcludingTax)
    # print("price Including taxes =" + priceIncludingTax)
    # if availability[:8] == "In stock":
    #     numberAvailable = availability[10:-11]
    # else:
    #     numberAvailable = 0
    # print(numberAvailable)
    # print("number of review is :" + reviewNumber)
    # print("url of this product is:" + productUrl)
    # print(category)
    # print(description)
    # print(imageUrl)
    # print(imageUrl.string)
    # print(type(imageUrl))
    # print(imageUrl.get('href'))
    # print(description[3].contents)


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
        del booksUrl[-1]
    if previous:
        del booksUrl[-1]
    for i in booksUrl:
        i = i.replace("../../../", "")
        if "https://books.toscrape.com/catalogue/"+i not in booksUrlList:
            booksUrlList.append("https://books.toscrape.com/catalogue/"+i)
    if next:
        urlNext = "https://books.toscrape.com/catalogue/category/books/" + category + "/" + booksUrl[-1]
        getBooksUrl(urlNext, booksUrlList, category)


# main(homePageUrl)
product("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", "travel")
