from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials

from scraper import (
    scrape_flipkart,
    scrape_amazon,
    scrape_nykaa,
    scrape_pharmeasy,
    scrape_meesho,
    scrape_snapdeal,
    scrape_netmeds,
    scrape_zepto,
    scrape_jiomart,
    scrape_myntra
)

app = Flask(__name__)

# Path to the Firebase service account JSON file
cred = credentials.Certificate('./recommend-me-6969-firebase-adminsdk.json')  
firebase_admin.initialize_app(cred)

@app.route('/api/scrape', methods=['GET'])
def scrape():
    query = request.args.get('query')
    category = request.args.get('category')
    products = []

    if not query or not category:
        return jsonify({"message": "Missing query or category parameter"}), 400

    if category == 'Clothes':
        print("Scraping clothes category")
        products += scrape_flipkart(query)
        products += scrape_amazon(query)
        products += scrape_myntra(query)
        products += scrape_meesho(query)
    elif category == 'Medicine':
        print("Scraping medicine category")
        products += scrape_pharmeasy(query)
        products += scrape_netmeds(query)
    elif category == 'Electronic':
        print("Scraping electronic category")
        products += scrape_flipkart(query)
        products += scrape_amazon(query)
        products += scrape_jiomart(query)
    elif category == 'Cosmetics':
        print("Scraping cosmetics category")
        products += scrape_nykaa(query)
    elif category == 'Grocery':
        print("Scraping grocery category")
        products += scrape_zepto(query)
        products += scrape_jiomart(query)
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
