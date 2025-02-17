# Cheap Mart

This project is a web application built with Flask that scrapes product data from e-commerce websites using Selenium. It allows users to search for products across multiple platforms, display the results, compare prices, and recommend the cheapest option using visual charts.

## Features
- **Web scraping with Selenium** to gather product data from BigBasket, Swiggy, and Zepto.
- **Flask backend** to handle HTTP requests and render templates.
- **Interactive web interface** with HTML, CSS, and JavaScript.
- **Price comparison** across platforms to recommend the cheapest product.
- **Data visualization** with charts to compare product prices.
- **Data storage in JSON** for scraped product details.

## Project Structure
```
flask scrap/
|-- app.py                  # Main Flask application
|-- scraper.py              # Selenium web scraper
|-- scraped_products.json   # JSON file storing scraped data
|-- static/
|   |-- app.js              # Frontend JavaScript
|   |-- style.css           # CSS styles
|-- templates/
    |-- index.html          # HTML template
```

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/thanigaivelan2004/flask-scraper.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd flask-scraper
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the application:**
   ```bash
   python app.py
   ```
2. **Access the web app** at `http://127.0.0.1:5000`.
3. **Search for products** by entering a product name and hitting search.
4. **View product comparisons** and recommended platforms based on price through visual charts.

## Dependencies
- Flask
- Selenium
- WebDriver Manager
- Bootstrap
- Chart.js

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
- **GitHub:** [thanigaivelan2004](https://github.com/thanigaivelan2004)
- **LinkedIn:** [Thanigaivelan P](https://www.linkedin.com/in/thanigaivelan-p-36014624a/)
- **Email:** thanigaivelan2004@gmail.com

---

*Happy Scraping!*

