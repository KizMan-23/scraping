from selenium import webdriver
from bs4 import BeautifulSoup
import time

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

driver = webdriver.Chrome()  # Or any other browser driver
driver.get(watch_url)

time.sleep(4)
# page_sour = driver.page_source
# with open("initial_source.html", "w+", encoding='utf-8') as file:
#     file.write(page_sour)

with open('initial_source.html') as file:
    ori = file.read()

soup = BeautifulSoup(ori, 'lxml')
content = soup.find_all('div')

links = soup.find_all("a", href=True)

product_links = []

for link in links:
    if "/ip/" in link["href"]:
        if "https" in link['href']:
            full_link = link['href']
        else:
            full_link = "https://walmart.com" + link['href']
        product_links.append(full_link)


product_des = soup.find_all('div', class_ = 'lh-copy dark-gray mv1 f4 mh0-l mh3 b')


print(product_des)
print(product_links[0])
