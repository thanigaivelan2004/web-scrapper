from flask import Flask, render_template, request, jsonify
import json
from scraper import scrape_site, launch_browser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')

    driver = launch_browser()
    all_products = []

    sites = {
        'bigbasket': f"https://www.bigbasket.com/ps/?q={search_term}&nc=as",
        'swiggy': f"https://www.swiggy.com/instamart/search?query={search_term}",
        'zepto': f"https://www.zeptonow.com/search?query={search_term}"
    }
    
    for site_name, search_url in sites.items():
        products = scrape_site(driver, search_url, site_name)
        all_products.extend(products)

    driver.quit()

    return jsonify(all_products)

if __name__ == "__main__":
    app.run(debug=True)