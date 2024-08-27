from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

def scrape_nykaa(query):
    url = f'https://www.nykaa.com/search/result/?q={query}'
    
    options = webdriver.ChromeOptions()
    options.binary_location = os.path.abspath('./chrome-linux/chrome')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.productWrapper'))
        )
    except Exception:
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    product_elements = soup.find_all('div', class_='productWrapper')
    
    for element in product_elements:
        if len(products) >= 5:
            break

        name, price, image = None, None, 'Image not available'

        name_tag = element.find('div', class_='css-xrzmfa')
        if name_tag:
            name = name_tag.text.strip()
        
        price_tag = element.find('span', class_='css-111z9ua')
        if price_tag:
            price = price_tag.text.strip()
        
        img_tag = element.find('img', class_='css-11gn9r6')
        if img_tag:
            image = img_tag.get('src', 'Image not available')

        if name and price:
            products.append({'name': name, 'price': price, 'image': image, 'via': 'Nykaa'})

    return products

# if __name__ == "__main__":
#     query = 'vitamin c serum'
#     products = scrape_nykaa(query)
#     print(products)