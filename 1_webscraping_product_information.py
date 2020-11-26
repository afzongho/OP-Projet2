import requests
from bs4 import BeautifulSoup
import re


url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
response = requests.get(url)

html = response.content
soup = BeautifulSoup(html, 'html.parser')
#print(scraped.prettify())
print(url)
print("****************")
#print(scraped.find_all("title"))
#print(scraped.find("title").text.strip())

articles = soup.find_all("article", class_="product_page") #parent
for article in articles:
    #title = article.h3.a["title"]
    #print(title)
    img_url = article.find("img")["src"]
    print(img_url)
    print("****************")
    title = article.h1.text
    print(title)
    print("****************")
    product_information = article.find("table", class_="table table-striped") #retourne tous les elements de la balise table
    product_information_row = product_information.find_all("tr")
    upc_code = product_information_row[0].find("td").text
    print(upc_code)
    print("****************")
    price_including_tax = product_information_row[2].find("td").text
    price_excluding_tax = product_information_row[3].find("td").text
    print(price_including_tax)
    print("****************")
    print(price_excluding_tax)
    print("****************")
    number_available = product_information_row[5].find("td").text
    print(number_available)
    print("****************")
    product_description = article.find("div", class_= "sub-header").findNext("p").text
    print(product_description)
    print("****************")
    review_rating = article.find("p", class_= re.compile(r'star-rating'))
    nb_rating = len(review_rating.find_all("i"))
    print(nb_rating)
    print("****************")

category = soup.find("ul", class_="breadcrumb")
book_category = category.find_all("li")[-2].find("a").text
print(book_category)

with open('product.csv', 'w+') as outf:
    outf.write('product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url \n')
    outf.write(url + ',' + upc_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description + ',' + book_category + ',' +  str(nb_rating) + ',' + img_url + '\n')