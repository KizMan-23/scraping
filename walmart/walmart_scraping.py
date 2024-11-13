from bs4 import BeautifulSoup
import requests

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

response = requests.get(watch_url)
soup = BeautifulSoup(response.text, "html.parser")
main_page = soup.find_all('div', id='__next')
brand_name = soup.find('div', class_ = 'mt0 mh0-l mh3')
product_description = soup.find('div', class_ = 'lh-copy dark-gray mv1 f4 mh0-l mh3 b')

print(soupcls)
print(product_description)

#discount = 
#original_price = 
#rating =     #over 5
#available_colors = 
#metal_type = 




#enter each section
#general div with class: class="flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl"
#obtain name of the watch, normal_price, bonus_price, color, brand and any other meta data
