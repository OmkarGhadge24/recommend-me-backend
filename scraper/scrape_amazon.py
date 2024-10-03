import requests
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def scrape_amazon(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    url = f'https://www.amazon.in/s?k={query}'
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

    product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for element in product_elements:
        if len(products) >= 10:
            break

        name = element.find('span', class_='a-text-normal')
        price = element.find('span', class_='a-price-whole') or element.find('span', class_='a-price')
        image = element.find('img', class_='s-image')
        link = element.find('a', class_='a-link-normal', href=True)

        product_data = {
            'name': name.text.strip() if name else None,
            'price': price.text.strip() if price else None,
            'image': image['src'] if image else 'Image not available',
            'link': f"https://www.amazon.in{link['href']}" if link else 'Link not available',
            'via': 'Amazon'
        }

        if product_data['name'] and product_data['price']:
            products.append(product_data)

    return products

# if __name__ == "__main__":
#     query = 'sony camera'
#     products = scrape_amazon(query)
#     for product in products:
#         print(product)