import requests
import BeautifulSoup
url="https://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
print("2")

