import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def scrape_flipkart(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

    url = f"https://www.flipkart.com/search?q={query}"
    retries = 5
    delay = 5

    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            logging.warning(f"Rate limited. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    
    container_classes = ['_75nlfW', 'CGtC98', '_75nlfW LYgYA3', 'tUxRFH', '_1sdMkc LFEi7Z']
    name_classes = ['KzDlHZ', 'syl9yP', '_4rR01T', 'IRpwTa']
    price_classes = ['Nx9bqj _4b5DiR', 'Nx9bqj', '_30jeq3', '_1_WHN1']
    image_classes = ['DByuf4', '_53J4C-', '_396cs4', '_3exPp9']

    for container_class in container_classes:
        for item in soup.find_all(['a', 'div'], class_=container_class):
            try:
                name = next((item.find('div', class_=cls).text for cls in name_classes if item.find('div', class_=cls)), None)
                price = next((item.find('div', class_=cls).text for cls in price_classes if item.find('div', class_=cls)), None)
                image = next((item.find('img', class_=cls)['src'] for cls in image_classes if item.find('img', class_=cls)), None)
                product_link = f"https://www.flipkart.com{item.find('a', href=True)['href']}" if item.find('a', href=True) else None
                
                if name and price and image:
                    products.append({'name': name, 'price': price, 'image': image, 'link': product_link, 'via': 'Flipkart'})
                
                if len(products) >= 10:
                    return products

            except AttributeError:
                continue

    return products

# if __name__ == "__main__":
#     query = "iphone 15 128gb"
#     print(scrape_flipkart(query))