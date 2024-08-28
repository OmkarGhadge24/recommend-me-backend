from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_meesho(query):
    url = f'https://www.meesho.com/search?q={query}'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-dkrFOg.ProductList__GridCol-sc-8lnc8o-0.cokuZA.eCJiSA'))
        )
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []

    product_elements = soup.find_all('div', {'class': 'sc-dkrFOg ProductList__GridCol-sc-8lnc8o-0 cokuZA eCJiSA'})
    
    for element in product_elements:
        if len(products) >= 5:
            break

        name, price, image = None, None, 'Image not available'

        name_div = element.find('div', class_='NewProductCardstyled__ProductHeaderWrapper-sc-6y2tys-30 gspQJ')
        if name_div:
            name_tag = name_div.find('p', class_='sc-eDvSVe gQDOBc NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5 ejhQZU NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5 ejhQZU')
            if name_tag:
                name = name_tag.text.strip()
        
        price_tag = element.find('h5', class_='sc-eDvSVe dwCrSh')
        if price_tag:
            price = price_tag.text.strip()
        
        img_tag = element.find('img', {'alt': True})
        if img_tag:
            image = img_tag.get('src', 'Image not available')

        if name and price:
            products.append({'name': name, 'price': price, 'image': image, 'via': 'Meesho'})

    return products

# if __name__ == "__main__":
#     query = 'shoes for men'
#     products = scrape_meesho(query)
#     print(products)