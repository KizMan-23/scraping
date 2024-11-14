from selenium import webdriver
from bs4 import BeautifulSoup
import time

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

# driver = webdriver.Chrome()  # Or any other browser driver
# driver.get(watch_url)

# time.sleep(4)
# # page_sour = driver.page_source
# # with open("initial_source.html", "w+", encoding='utf-8') as file:
# #     file.write(page_sour)

with open('initial_source.html') as file:
    ori = file.read()

soup = BeautifulSoup(ori, 'lxml')
content = soup.find_all('div') 

#How do I access the scripts in content...!!!

print(content)

links = content.find_all("a", href=True)

def get_links (links):
    product_links = []

    for link in links:
        if "/ip/" in link["href"]:
            if "https" in link['href']:
                full_link = link['href']
            else:
                full_link = "https://walmart.com" + link['href']
            product_links.append(full_link)

    return product_links

prod_links = get_links(links)


product_des = content.find_all('div', class_ = 'lh-copy dark-gray mv1 f4 mh0-l mh3 b')


print(product_des)
print(prod_links[0])
