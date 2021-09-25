import requests
from bs4 import BeautifulSoup
url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
availability=soup.find("p",class_="instock availability")
price=soup.find("p",class_="price_color")
description=soup.find_all("p")[-1]
title=soup.find("h1")
productInformation=soup.find("tr",class_="table table-striped")
#productUrl=
#upc=
#priceIncludingTax=
#priceExcludingTax=
#NumberAvailable=
#category=
#reviewRating=
#imageUrl=soup.find("div",class_="item active")
#print (title.string)
#print (price.string)
#print(availability.string)
#print(description.string)
#print(imageUrl.string)
print(productInformation)
