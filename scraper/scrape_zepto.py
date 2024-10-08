from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_zepto(query):
    url = f'https://www.zeptonow.com/search?query={query}'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="product-card"]'))
        )
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    product_elements = soup.find_all('a', class_='!my-0 relative my-3 mb-9 rounded-t-xl rounded-b-md group')
    
    for element in product_elements:
        if len(products) >= 10:
            break

        name, price, image, link = None, None, 'Image not available', None

        name_tag = element.find('h5', class_='font-subtitle text-lg tracking-wider line-clamp-2 !text-base !font-semibold !h-9 !tracking-normal px-1.5')
        if name_tag:
            name = name_tag.text.strip()
        
        price_tag = element.find('h4', class_='font-heading text-lg tracking-wide line-clamp-1 !font-semibold !text-md !leading-4 !m-0')
        if price_tag:
            price = price_tag.text.strip()
        
        img_tag = element.find('img', {'alt': True})
        if img_tag:
            image = img_tag.get('src', 'Image not available')

        link_tag = element.get('href')
        if link_tag:
            link = f'https://www.zeptonow.com{link_tag}'  # Construct the full URL

        if name and price:
            products.append({'name': name, 'price': price, 'image': image, 'link': link, 'via': 'Zepto'})

    return products

# if __name__ == "__main__":
#     query = 'mango juice'
#     products = scrape_zepto(query)
#     print(products)
