from bs4 import BeautifulSoup
import requests
import csv
import json

watch_url = "https://www.walmart.com/ip/OLEVS-Mens-Watches-Chronograph-Business-Dress-Quartz-Stainless-Steel-Waterproof-Luminous-Date-Wrist-Watch-For-Men-Blue-Dial/5303331858?classType=VARIANT&athbdg=L1600&adsRedirect=true"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}


def get_product_url(query, page_number=1):
    try:
        base_url = "https://www.walmart.com"
        search_url = f"https://www.walmart.com/search?q={query}&page={page_number}&affinityOverride=default"
        response = requests.get(search_url, headers = HEADERS)
        soup1 = BeautifulSoup(response.text, "html.parser")
        links  = soup1.find_all("a", href=True)

        page_links = []
        full_url = ()
        seen_url = set()

        for link in links:
            if "/ip/" in link['href']:
                if "https" in link['href']:
                    full_url = link['href']
                else:
                    full_url = base_url + link['href']

                if full_url not in seen_url:
                    page_links.append(full_url)

        print(f"Length of {len(page_links)} Links in page {page_number}")

        full_page_links = [link for link in page_links if link and link.startswith("https://")]

        print(f"Length of {len(full_page_links)} full_page_link...Starts ")
    except Exception as e:
        print(f"Error {e} occured in page {page_number}")

    return page_links


def get_product_info(product_url):
    print(f"Processing URL: , {product_url}")

    response = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    main_page = soup.find('div', id= "__next")

    product_description = None
    brand_name = None
    product_img_url = []
    discount_price = None
    original_price = None
    avg_rating = None
    number_of_reviews = None
    product_details = []
    available_colors = []

    #USING TRY-EXCEPT TO FORM A DYNAMIC CODE FOR PRODUCT LINKS THAT MAY NOT HAVE SOME DATA IN ITS PROFILE

    try:
        product_description = main_page.find('h1', class_='lh-copy dark-gray mv1 f4 mh0-l mh3 b').text
    except AttributeError:
        pass 

    try:
        brand_name = main_page.find("div", class_="mt0 mh0-l mh3").text
    except AttributeError:
        pass

    try:
        image_container = main_page.find_all('img')
        format_description = product_description.replace(" ", "-").lower() if product_description else ""
        for img in image_container:
            img_url = img.get("src")
            if "https://i5.walmartimages.com/seo/" in img_url and format_description in img_url.lower():
                if img_url not in product_img_url:
                    product_img_url.append(img_url)
    except AttributeError:
        pass 

    try:
        discount_price = main_page.find("span", class_="inline-flex flex-column").text.split()[1]
    except (AttributeError, IndexError):
        pass

    try:
        original_price = main_page.find("span", class_="mr2 f6 gray strike").text
    except AttributeError:
        pass

    try:
        rating = main_page.find("span", class_="f7 ph1")
        avg_rating = rating.text
    except AttributeError:
        pass

    try:
        number_of_reviews = main_page.find("div", class_="flex items-center mr2").find("a", href=True).text
    except AttributeError:
        pass

    try:
        details  = main_page.find("div", class_ = "flex flex-wrap dark-gray")
        place_a = details.find("div", class_ = "f6 tc flex justify-center")
        while place_a:
            product_details.append(place_a.get_text(strip=True))
            place_a = place_a.find_next_sibling("div", class_ = "f6 tc flex justify-center")
    except AttributeError:
        pass

    try:
        option_list = main_page.find("div", class_="flex flex-wrap nl1 nr1")
        option_a = option_list.find("div", class_="flex flex-column bg-white")
        while option_a:
            available_colors.append(option_a.get_text(strip=True))
            option_a = option_a.find_next_sibling("div", class_="flex flex-column bg-white")
    except AttributeError:
        pass 

    product_info = {
        "brand_name": brand_name,
        "product_description": product_description,
        "product_price": original_price,
        "product_discount_price": discount_price,
        "rating_avg": avg_rating,
        "nos_of_reviews": number_of_reviews,
        "image_url": product_img_url,
        "color_and_materials": product_details, 
        "available_colors": available_colors
    }

    return product_info

search_queries = ["laptops", "cameras", 'keyboard', "computer", "television", "speakers", "power bank"]

def main():
     # Saving data into JSON and CSV
    for prd in search_queries:

        min_page_number = 15
        QUERY = prd
        page_number = 1

        name = str(QUERY).replace(" ", "_").lower()

        print("Searching as current query", QUERY)

        # Open JSON and CSV files outside the loop in append mode
        with open(f"{name}_data.json", "a", encoding='utf-8') as json_file, \
            open(f"{name}_data.csv", "a", encoding='utf-8', newline='') as csv_file:

            csv_writer = csv.writer(csv_file)

            while page_number < min_page_number:
                print(f"Searching page {page_number}")
                product_links = get_product_url(query=QUERY, page_number=page_number)

                for link in product_links:
                    product_info = get_product_info(link) 

                    json_file.write(json.dumps(product_info) + "\n")

                    csv_writer.writerow(product_info.values())

                page_number += 1
                #THE PRODUCT IS OF ONLY 7 PAGES

if __name__ == "__main__":
    main()
