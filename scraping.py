import requests
from bs4 import BeautifulSoup
homePageUrl = "https://books.toscrape.com/catalogue/page-1.html"
homePage = requests.get(homePageUrl)
soup = BeautifulSoup(homePage.content, "html.parser")
categoryList = soup.find_all("a")
print(categoryList[-50].string)
print(len(categoryList))
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
description = soup.find_all("p")[-1].string
title = soup.find("h1").string
productInformation = soup.find_all("td")
productUrl = url
upc = productInformation[0].string
priceIncludingTax = productInformation[3].string
priceExcludingTax = productInformation[2].string
availability = productInformation[5].string
reviewNumber = productInformation[6].string
# NumberAvailable=
# category =
# reviewRating=
imageUrl = soup.find("img")
print("upc = "+upc)
print("title = "+title)
print("price excluding taxes ="+priceExcludingTax)
print("price Including taxes ="+priceIncludingTax)
print("availability :"+availability)
print("number of review is :"+reviewNumber)
print("description is:"+description)
print("url of this product is:"+productUrl)
print(imageUrl)
print(imageUrl.string)
