from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_netmeds(query):
    url = f'https://www.netmeds.com/catalogsearch/result/{query}/all'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cat-item'))
        )
    except Exception:
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    product_elements = soup.find_all('div', class_='cat-item')
    
    for element in product_elements:
        if len(products) >= 10:
            break

        name, price, image, link = None, None, 'Image not available', None

        name_tag = element.find('h3', class_='clsgetname')
        if name_tag:
            name = name_tag.text.strip()
        
        price_tag = element.find('span', class_='final-price')
        if price_tag:
            price = price_tag.text.strip()
        
        img_tag = element.find('img', class_='product-image-photo')
        if img_tag:
            image = img_tag.get('src', 'Image not available')
        
        link_tag = element.find('a', class_='category_name')
        if link_tag:
            link = link_tag.get('href', None)
            if link:
                link = 'https://www.netmeds.com' + link

        if name and price:
            products.append({'name': name, 'price': price, 'image': image, 'link': link, 'via': 'Netmeds'})

    return products

# if __name__ == "__main__":
#     query = 'paracetemol'
#     products = scrape_netmeds(query)
#     print(products)
