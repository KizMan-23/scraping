from bs4 import BeautifulSoup
import requests

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}

search_url = "https://www.walmart.com/search?q=watches%20for%20men&page=1&affinityOverride=default"
min_page_number = 99
query = "watches for men"

# def get_product_url(query, page_number=1):
base_url = "https://www.walmart.com"
search_url = f"https://www.walmart.com/search?q={query}&page=1&affinityOverride=default"
response = requests.get(search_url, headers = HEADERS)
soup1 = BeautifulSoup(response.text, "html.parser")
links  = soup1.find_all("a", href=True)

page_link = []
full_url = ()

for link in links:
    if "/ip/" in link['href']:
        if "https" in link['href']:
            full_url = link['href']
        else:
            full_url = base_url + link['href']
    page_link.append(full_url)

print(len(page_link))



def get_product_info(product_url):
    response = requests.get(watch_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    main_page = soup.find('div', id= "__next")
    image_container = main_page.find_all('img')


    product_description = main_page.find('h1', class_ = 'lh-copy dark-gray mv1 f4 mh0-l mh3 b').text
    #Lesson: "find_all" returns a list of contents. Better to use "find"
    brand_name = main_page.find("div", class_= "mt0 mh0-l mh3").text

    product_img_url = []
    for img in image_container:
        format_description = product_description.replace(" ", "-").lower()
        img_url = img.get("src")

        if "https://i5.walmartimages.com/seo/" in img_url:
            if format_description in img_url.lower():
                all_link = img_url
                if all_link not in product_img_url:
                    product_img_url.append(all_link)
        
    product_image = requests.get(product_img_url[0]).content #returns binary data of the image. use "wb" to write the binary code to a ".jpg"

    discount_price = main_page.find("span", class_ = "inline-flex flex-column").text.split()[1]
    original_price = main_page.find("span", class_ = "mr2 f6 gray strike").text
    rating = main_page.find("span", class_ = "f7 ph1")
    avg_rating = rating.text
    number_of_reviews = rating.find_parent("div", class_ = "flex items-center mr2").find("a", href=True).text
    color = main_page.find("div", class_ = "mid-gray mb2").text.split()[1]

    option_list = main_page.find("div", class_ = "flex flex-wrap nl1 nr1")
    option_a = option_list.find("div", class_ = "flex flex-column bg-white")

    available_colors = []
    while option_a:
        available_colors.append(option_a.get_text(strip=True))
        option_a = option_a.find_next_sibling("div", class_ = "flex flex-column bg-white")

    

# if __name__ == "__main__":
#     main()
