import requests
from bs4 import BeautifulSoup

def scrape_pharmeasy(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://pharmeasy.in/search/all?name={query}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    container_class = 'ProductCard_medicineUnitContainer__cBkHl'
    name_class = 'ProductCard_medicineName__8Ydfq'
    price_class = 'ProductCard_ourPrice__yDytt'
    image_class = 'ProductCard_productImage__dq5lq'
    
    for item in soup.find_all('div', class_=container_class):
        try:
            name_tag = item.find('h1', class_=name_class)
            price_tag = item.find('div', class_=price_class)
            image_tag = item.find('img', class_=image_class)
            link_tag = item.find('a', href=True)

            name = name_tag.text if name_tag else 'No name available'
            price = price_tag.text.strip() if price_tag and '₹' in price_tag.text else None
            image = image_tag['src'] if image_tag else 'Image not available'
            product_link = f"https://pharmeasy.in{link_tag['href']}" if link_tag else 'No link available'

            if price:  # Ensure price is not None or empty
                products.append({
                    'name': name,
                    'price': price,
                    'image': image,
                    'link': product_link,
                    'via': 'PharmEasy'
                })

            if len(products) == 10:
                return products

        except AttributeError:
            continue

    return products

# if __name__ == "__main__":
#     query = "paracetamol"
#     products = scrape_pharmeasy(query)
#     print(products)