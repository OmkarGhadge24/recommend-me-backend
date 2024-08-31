import requests
from bs4 import BeautifulSoup
import re

def scrape_snapdeal(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://www.snapdeal.com/search?clickSrc=top_searches&keyword={query.replace(' ', '%20')}&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    sections = soup.find_all('section')
    for section in sections:
        items = section.find_all('div', class_='col-xs-6 favDp product-tuple-listing js-tuple')
        for item in items:
            try:
                title_tag = item.find('p', class_='product-title')
                name = title_tag.text.strip() if title_tag else 'No name available'

                price_tag = item.find('div', class_='product-price-row')
                discounted_price_tag = price_tag.find('span', class_='product-price') if price_tag else None
                discounted_price = discounted_price_tag.text.strip() if discounted_price_tag else 'No price available'
                
                # Extract numeric price
                numeric_price = re.sub(r'[^\d]', '', discounted_price)

                img_tag = item.find('img', class_='product-image')
                if img_tag:
                    image = img_tag.get('src', 'Image not available')
                    if image == 'Image not available':
                        image = img_tag.get('srcset', 'Image not available')
                else:
                    image_tag = item.find('input', class_='compareImg')
                    image = image_tag.get('value', 'Image not available') if image_tag else 'Image not available'

                link_tag = item.find('a', class_='dp-widget-link')
                link = link_tag.get('href', 'Link not available') if link_tag else 'Link not available'
                link = f"https://www.snapdeal.com{link}"  # Correct link format

                if name and numeric_price and image and link:
                    products.append({'name': name, 'price': numeric_price, 'image': image, 'link': link, 'via': 'Snapdeal'})
                    if len(products) == 5:
                        return products
            except AttributeError:
                continue

    return products

# if __name__ == "__main__":
#     query = "shirt for men"
#     products = scrape_snapdeal(query)
#     print(products)