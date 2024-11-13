from bs4 import BeautifulSoup
import requests
import json
import time

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}

response = requests.get(watch_url, headers=HEADERS)

with open("page_resp.text", "w+", encoding='utf-8') as file:
    file.write(response)


with open("page_resp.text") as f:
    rep = f.read()

soup = BeautifulSoup(rep.text, "html.parser")
main_page = soup.find_all('div', id='__next')

data = json.load(main_page)

# brand_name = soup.find_all('div', class_ = 'mt0 mh0-l mh3')

# product_description = soup.find_all('div', class_ = 'lh-copy dark-gray mv1 f4 mh0-l mh3 b')

print(data)
#print(brand_name)
#print(product_description)

#discount = 
#original_price = 
#rating =     #over 5
#available_colors = 
#metal_type = 



#enter each section
#general div with class: class="flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl"
#obtain name of the watch, normal_price, bonus_price, color, brand and any other meta data
