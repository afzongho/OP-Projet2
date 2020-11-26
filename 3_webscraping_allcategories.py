import requests
from bs4 import BeautifulSoup
import re
import shutil

def download_image(image,filename):
    response = requests.get(image, stream=True)
    realname = filename

    file = open("IMG/{}.jpg".format(realname), 'wb')

    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

#fonction quiva scraper tous les produits
def scrape_product(url):

    response = requests.get(url)

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all("article", class_="product_page") #parent
    for article in articles:
        #title = article.h3.a["title"]
        #print(title)
        img_url = article.find("img")["src"]
        img_url = img_url.replace("../../","https://books.toscrape.com/")
        title = article.h1.text

        product_information = article.find("table", class_="table table-striped") #retourne tous les elements de la balise table
        product_information_row = product_information.find_all("tr")
        upc_code = product_information_row[0].find("td").text

        price_including_tax = product_information_row[2].find("td").text
        price_excluding_tax = product_information_row[3].find("td").text


        number_available = product_information_row[5].find("td").text

        product_description = article.find("div", class_= "sub-header").findNext("p").text


        review_rating = article.find("p", class_= re.compile(r'star-rating'))
        nb_rating = len(review_rating.find_all("i"))



    category = soup.find("ul", class_="breadcrumb")
    book_category = category.find_all("li")[-2].find("a").text

    download_image(img_url,re.sub('["/:]',"a",title).split(" ")[0]+"_"+book_category)
    content = url + ';' + upc_code + ';' + title + ';' + price_including_tax + ';' + price_excluding_tax + ';' + number_available + ';' + product_description + ';' + book_category + ';' + str(
            nb_rating) + ';' + img_url + '\n'
    return content


#scraping category

def scraping_category(url):
    response = requests.get(url)

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')



    articles = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")  # parent
    content = ""
    for article in articles:
        h3 = article.find("h3")
        a = h3.find("a")
        href = a["href"]
        title = a["title"]
        href = href.replace("../../../","https://books.toscrape.com/catalogue/" )
        content += scrape_product(href)

    return content

def scraping_page(url):
    content = scraping_category(url)
    response = requests.get(url)

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    pager = soup.find("ul", class_="pager")
    if pager != None:
        li = pager.find("li", class_="current")
        max_page_array = " ".join(li.text.split()).split()
        #max_page_array = [ x for x in max_page_array if '\'\'' not in x and '\n' not in x ]
        max_page = max_page_array[len(max_page_array)-1]
        k = 1
        while k < int(max_page):
            url_page = url.replace("index.html","page-"+str(k+1)+".html")
            print(url_page)
            content += scraping_category(url_page)
            k += 1

    return content

response = requests.get("http://books.toscrape.com/index.html")

html = response.content
soup = BeautifulSoup(html, 'html.parser')

#fonction main pour structurer ton code

#scraping de chaque url/page catégorie

ul_parent = soup.find_all("ul", class_="nav nav-list")  # parent
ul = ul_parent[0].find("ul")
categories = ul.find_all("li")

content_all = ""
for categorie in categories:
    a = categorie.find("a")
    print(a.text.strip())
    url = a["href"]
    url = "http://books.toscrape.com/"+ url
    content_all += scraping_page(url)
    with open(a.text.strip() + ".csv", 'w+') as outf:
        outf.write(
            'product_page_url| universal_ product_code (upc)| title| price_including_tax| price_excluding_tax| number_available| product_description| category| review_rating| image_url \n')
        outf.write(content_all)