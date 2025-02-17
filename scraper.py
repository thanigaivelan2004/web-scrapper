import logging
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def launch_browser():
    """Launch Chrome browser with configurations."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.page_load_strategy = 'eager'

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for element to be present and return it."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        logging.warning(f"Timeout waiting for element: {selector}")
        return None

def scrape_site(driver, search_url, site_name):
    """Scrape product data from a given site."""
    driver.get(search_url)
    time.sleep(5)  # Initial wait for page load

    products_data = []
    max_products = 3 # Stop after finding 3 products
    scroll_attempts = 0
    max_scroll_attempts = 10  # Limit scrolling attempts to avoid excessive time consumption

    while len(products_data) < max_products and scroll_attempts < max_scroll_attempts:
        scroll_attempts += 1

        try:
            # Get current scroll position
            current_position = driver.execute_script("return window.pageYOffset;")

            # Scroll down
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)  # Allow time for images and elements to load

            # Scrape products
            current_products = scrape_products(driver, site_name)

            for product in current_products:
                if len(products_data) < max_products:
                    if product not in products_data:
                        products_data.append(product)

            # Get new scroll height and position
            scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")
            current_position = driver.execute_script("return window.pageYOffset;")

            # Log progress
            logging.info(f"Scroll attempt {scroll_attempts}/{max_scroll_attempts}, "
                         f"Position: {current_position}/{scroll_height}")

        except Exception as e:
            logging.error(f"Error during scrolling: {e}")

    logging.info(f"Final products found: {len(products_data)}")
    return products_data

def scrape_products(driver, site_name):
    """Scrape product data including images."""
    products_data = []

    try:
        if site_name == 'bigbasket':
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.mt-5 li')
        elif site_name == 'blinkit':
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Product__UpdatedPlpProductContainer-sc-11dk8zk-0')
        elif site_name == 'swiggy':
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'div.XjYJe')
        elif site_name == 'zepto':
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'a.\\!my-0')
        else:
            return products_data

        for li in li_elements:
            try:
                # Extract product details
                if site_name == 'bigbasket':
                    product_details_text = li.find_element(By.XPATH, './/h3').text if li.find_elements(By.XPATH, './/h3') else "No Product Details"
                    details_split = product_details_text.split("\n")
                    product_name = li.find_element(By.CSS_SELECTOR, 'h3').text.strip()
                    product_link = li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    image_url = li.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    quantity = details_split[4] if len(details_split) > 4 else "No Pack Details"

                    mrp = safe_extract(li, './/span[contains(@class,"Pricing___StyledLabel2-sc-pldi2d-2")]', "No Original Price")
                    discounted_price = safe_extract(li, './/span[contains(@class,"Pricing___StyledLabel-sc-pldi2d-1")]', "No Discounted Price")
                    offer = safe_extract(li, './/span[contains(text(),"OFF")]', "No Offer")
                    company_name = safe_extract(li, './/span[contains(@class,"BrandName___StyledLabel2-sc-hssfrl-1")]', "No Company Name")
                elif site_name == 'blinkit':
                    product_name = li.find_element(By.CSS_SELECTOR, 'div.Product__UpdatedTitle-sc-11dk8zk-9').text.strip()
                    product_link = li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    image_url = li.find_element(By.CSS_SELECTOR, '.Imagestyles__ImageContainer-sc-1u3ccmn-0 img').get_attribute('src')
                    quantity = safe_extract(li, 'span', "No Pack Details")
                    mrp = safe_extract(li, '.Product__UpdatedPriceAndAtcContainer-sc-11dk8zk-10 div div:nth-of-type(2)', "No Original Price")
                    discounted_price = safe_extract(li, '.Product__UpdatedPriceAndAtcContainer-sc-11dk8zk-10 div div:nth-of-type(1)', "No Discounted Price")
                    offer = safe_extract(li, 'div.Product__UpdatedOfferTitle-sc-11dk8zk-2', "No Offer")
                    company_name = "N/A"
                elif site_name == 'swiggy':
                    try:
                        product_name = li.find_element(By.CSS_SELECTOR, 'div.kyEzVU').text.strip()  # Extract product name
                    except Exception:
                        product_name = "No Product Name"
                        
                    try:
                        # Using WebDriverWait to wait for the product link element to be visible
                        product_link = li.get_attribute('href')

                        if not product_link:
                            product_link = "No Product Link"
                    except Exception as e:
                        product_link = "No Product Link"
                        print(f"Error extracting product link: {e}")
                        
                    try:
                        image_url = li.find_element(By.CSS_SELECTOR, 'img.ibghhT').get_attribute('src')  # Extract image URL
                    except Exception:
                        image_url = "No Image URL"
                        
                    try:
                        quantity = li.find_element(By.CSS_SELECTOR, 'div.entQHA').text.strip()  # Extract pack details (quantity)
                    except Exception:
                        quantity = "No Pack Details"
                        
                    try:
                        mrp = li.find_element(By.CSS_SELECTOR, 'div.hQJHwx').text.strip()  # Extract original price (MRP)
                    except Exception:
                        mrp = "No Original Price"
                        
                    try:
                        discounted_price = li.find_element(By.CSS_SELECTOR, 'div.jLtxeJ').text.strip()  # Extract discounted price
                    except Exception:
                        discounted_price = "No Discounted Price"
                        
                    try:
                        offer = li.find_element(By.CSS_SELECTOR, 'div.cNzAGo').text.strip()  # Extract the offer details (e.g., discount info)
                    except Exception:
                        offer = "No Offer"
                        
                    try:
                        company_name = li.find_element(By.CSS_SELECTOR, 'div.kyEzVU').text.strip()  # Extract company name
                    except Exception:
                        company_name = "No Company Name"
                elif site_name == 'zepto':
                    try:
                        product_name = li.find_element(By.CSS_SELECTOR, 'h5[data-testid="product-card-name"]').text.strip()
                    except:
                        product_name = "No Product Name"

                    product_link = li.get_attribute('href')

                    try:
                        image_url = li.find_element(By.CSS_SELECTOR, 'img.rounded-lg').get_attribute('src')
                    except:
                        image_url = "No Image URL"

                    try:
                        quantity = li.find_element(By.CSS_SELECTOR, 'span[data-testid="product-card-quantity"] h4').text.strip()
                    except:
                        quantity = "No Pack Details"

                    try:
                        mrp_element = li.find_elements(By.CSS_SELECTOR, 'p.line-through')
                        mrp = mrp_element[0].text.strip() if mrp_element else "No Original Price"
                    except:
                        mrp = "No Original Price"

                    try:
                        discounted_price = li.find_element(By.CSS_SELECTOR, 'h4[data-testid="product-card-price"]').text.strip()
                    except:
                        discounted_price = "No Discounted Price"

                    try:
                        offer_element = li.find_elements(By.CSS_SELECTOR, 'p.absolute.top-0.text-center.text-white')
                        offer = offer_element[0].text.strip() if offer_element else "No Offer"
                    except:
                        offer = "No Offer"

                    # Extracting company name from the first word of the product name
                    company_name = product_name.split()[0] if product_name and product_name != "No Product Name" else "N/A"

                # Store structured product data with error handling for each field
                product_data = {
                    "Product Name": product_name,
                    "Quantity": quantity,
                    "MRP": mrp,
                    "Discounted Price": discounted_price,
                    "Offer": offer,
                    "Company Name": company_name,
                    "Image URL": image_url,
                    "Product Link": product_link,
                    "Site": site_name
                }

                products_data.append(product_data)
            except Exception as e:
                logging.warning(f"Error extracting product data: {e}")
                continue

    except Exception as e:
        logging.error(f"Error finding product elements: {e}")

    return products_data

def safe_extract(element, xpath, default=""):
    """Safely extract text from an element using xpath."""
    try:
        return element.find_element(By.XPATH, xpath).text
    except (NoSuchElementException, Exception):
        return default

def save_to_json(data, filename):
    """Save data to JSON file."""
    try:
        if not data:
            logging.warning("No data to save in JSON.")
            return

        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"JSON save error: {e}")

def main():
    driver = None
    try:
        driver = launch_browser()
        search_term = "almond"
        sites = {
            'bigbasket': f"https://www.bigbasket.com/ps/?q={search_term}&nc=as",
            'swiggy': f"https://www.swiggy.com/instamart/search?query={search_term}",
            'zepto': f"https://www.zeptonow.com/search?query={search_term}"
        }

        all_products = []
        for site_name, search_url in sites.items():
            logging.info(f"Scraping {site_name}...")
            products = scrape_site(driver, search_url, site_name)
            all_products.extend(products)

        if all_products:
            logging.info(f"Total products found: {len(all_products)}")
            # Save the data
            save_to_json(all_products, "products.json")
        else:
            logging.error("No products found.")

    except Exception as e:
        logging.error(f"Scraping process failed: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()