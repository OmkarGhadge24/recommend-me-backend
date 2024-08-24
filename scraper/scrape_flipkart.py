import requests
from bs4 import BeautifulSoup
import time

def scrape_flipkart(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://www.flipkart.com/search?q={query}"
    retries = 5
    delay = 5
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            print(f"Rate limited. Attempt {attempt + 1}/{retries}. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            print(f"Unexpected status code: {response.status_code}")
            return []
    else:
        print("Failed to fetch the page after multiple attempts.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    container_classes = ['_75nlfW', 'CGtC98', '_75nlfW LYgYA3']
    name_classes = ['KzDlHZ', 'syl9yP']
    price_classes = ['Nx9bqj _4b5DiR', 'Nx9bqj']
    image_classes = ['DByuf4', '_53J4C-']

    for container_class in container_classes:
        for item in soup.find_all(['a', 'div'], class_=container_class):
            if len(products) >= 5:
                return products
            try:
                name = None
                for name_class in name_classes:
                    name_tag = item.find('div', class_=name_class)
                    if name_tag:
                        name = name_tag.text
                        break
                price = None
                for price_class in price_classes:
                    price_tag = item.find('div', class_=price_class)
                    if price_tag:
                        price = price_tag.text
                        break
                image = None
                for image_class in image_classes:
                    image_tag = item.find('img', class_=image_class)
                    if image_tag:
                        image = image_tag['src']
                        break
                if name and price and image:
                    products.append({'name': name, 'price': price, 'image': image , 'via':'Flipkart'})
            except AttributeError:
                continue

    return products

# if __name__ == "__main__":
#     query = "face wash"
#     print(scrape_flipkart(query))