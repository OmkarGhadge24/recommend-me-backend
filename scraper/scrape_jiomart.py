from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_jiomart(query):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = f"https://www.jiomart.com/search/{query}"
    driver.get(url)
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []
    container_class = 'ais-InfiniteHits-item'
    name_class = 'plp-card-details-name'
    price_class = 'jm-heading-xxs jm-mb-xxs'
    image_class = 'lazyautosizes'
    link_tag = 'a'

    for item in soup.find_all('li', class_=container_class):
        try:
            name = item.find('div', class_=name_class).text.strip() if item.find('div', class_=name_class) else 'No name available'
            price = item.find('span', class_=price_class).text.strip() if item.find('span', class_=price_class) else 'Price not available'

            image_tag = item.find('img', class_=image_class)
            if image_tag:
                image = image_tag.get('src') or image_tag.get('data-src') or image_tag.get('data-lazy-src')
            else:
                image = 'Image not available'

            product_link = f"https://www.jiomart.com{item.find(link_tag, href=True)['href']}" if item.find(link_tag, href=True) else 'No link available'

            products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': product_link,
                'via': 'JioMart'
            })

            if len(products) >= 5:
                break

        except AttributeError:
            continue

    return products

# if __name__ == "__main__":
#     query = "bluetooth headphone"
#     products = scrape_jiomart(query)
#     print(products)
