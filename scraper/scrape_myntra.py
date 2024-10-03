from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.parse

def scrape_myntra(query):
    encoded_query = urllib.parse.quote(query)
    url = f'https://www.myntra.com/{encoded_query}?rawQuery={encoded_query}'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-base'))
        )
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    product_elements = soup.find_all('li', class_='product-base')
    
    for element in product_elements:
        if len(products) >= 10:
            break

        price, image, link = None, 'Image not available', None
        brand, name = None, None

        link_tag = element.find('a', href=True)
        if link_tag:
            link = "https://www.myntra.com" + link_tag['href']
        
        brand_tag = element.find('h3', class_='product-brand')
        if brand_tag:
            brand = brand_tag.text.strip()
        
        name_tag = element.find('h4', class_='product-product')
        if name_tag:
            name = name_tag.text.strip()
        
        price_tag = element.find('span', class_='product-discountedPrice')
        if price_tag:
            price = price_tag.text.strip()
        
        img_tag = element.find('img', {'alt': True})
        if img_tag:
            image = img_tag.get('src', 'Image not available')

        # Combine brand and product name
        if brand and name:
            combined_name = f"{brand} - {name}"
        else:
            combined_name = name or brand or "Name not available"

        if price and link:
            products.append({
                'name': combined_name,
                'price': price,
                'image': image,
                'link': link,
                'via': 'Myntra'
            })

    return products

# if __name__ == "__main__":
#     query = 'kurta for boys'
#     products = scrape_myntra(query)
#     print(products)
