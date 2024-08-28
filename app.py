from flask import Flask, request, jsonify
from scraper import (
    scrape_flipkart,
    scrape_amazon,
    scrape_nykaa,
    scrape_pharmeasy,
    scrape_meesho,
    scrape_snapdeal,
    scrape_netmeds,
    scrape_zepto
)

app = Flask(__name__)

@app.route('/api/scrape', methods=['GET'])
def scrape():
    query = request.args.get('query')
    category = request.args.get('category')
    products = []

    print(f"Received query: {query}, category: {category}")

    if category == 'Clothes':
        print("Scraping clothes category")
        products += scrape_flipkart(query)
        products += scrape_amazon(query)
        products += scrape_meesho(query)
    elif category == 'Medicine':
        print("Scraping medicine category")
        products += scrape_pharmeasy(query)
        products += scrape_netmeds(query)
    elif category == 'Electronic':
        print("Scraping electronic category")
        products += scrape_flipkart(query)
        products += scrape_amazon(query)
    elif category == 'Cosmetics':
        print("Scraping cosmetics category")
        products += scrape_nykaa(query)
        products += scrape_snapdeal(query)
    elif category == 'Grocery':
        print("Scraping Grocery category")
        products += scrape_zepto(query)
        products += scrape_amazon(query)
    else:
        print("Scraping others categories")
        products += scrape_amazon(query)
        products += scrape_flipkart(query)
        products += scrape_snapdeal(query)
        products += scrape_meesho(query)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)