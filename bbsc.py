import logging
import csv
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USE_PROXY = False
MAX_RETRIES = 3
SCROLL_ATTEMPTS = 5


def launch_browser():
    """Launch Chrome browser with configurations."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def extract_categories(driver):
    """Extract categories from BigBasket."""
    try:
        driver.get("https://www.bigbasket.com/")
        time.sleep(5)
        
        category_buttons = [
            "#headlessui-menu-button-\\:R5bab6\\:",
            "button.category-toggle",
            ".category-menu-btn"
        ]
        
        for button_selector in category_buttons:
            try:
                category_button = driver.find_element(By.CSS_SELECTOR, button_selector)
                category_button.click()
                time.sleep(3)
                break
            except:
                continue

        category_links = driver.find_elements(By.CSS_SELECTOR, "ul.jsx-1259984711 a.CategoryTree___StyledLink-sc-8wbym9-0")
        
        scraped_categories = []
        for category in category_links:
            name = category.text.strip()
            link = category.get_attribute('href')
            if link and not link.startswith("http"):
                link = f"https://www.bigbasket.com{link}"
            
            if name and link:
                scraped_categories.append({"name": name, "link": link})
        
        return scraped_categories
    except Exception as e:
        logging.error(f"Category extraction failed: {e}")
        return []


def scrape_category_items(driver, category_link):
    """Scrape product data from a given category link."""
    driver.get(category_link)
    
    products_data = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@class="mt-5 grid gap-6 grid-cols-9"]/li'))
        )
    except:
        logging.warning("No products found on page.")
        return []
    
    li_elements = driver.find_elements(By.XPATH, '//ul[@class="mt-5 grid gap-6 grid-cols-9"]/li')
    
    for li in li_elements:
        try:
            product_data = {
                "Offer": li.find_element(By.XPATH, './/span[contains(text(),"OFF")]').text if li.find_elements(By.XPATH, './/span[contains(text(),"OFF")]') else "No Offer",
                "Company Name": li.find_element(By.XPATH, './/span[contains(@class,"BrandName___StyledLabel2-sc-hssfrl-1")]').text if li.find_elements(By.XPATH, './/span[contains(@class,"BrandName___StyledLabel2-sc-hssfrl-1")]') else "No Company Name",
                "Product Details": li.find_element(By.XPATH, './/h3').text if li.find_elements(By.XPATH, './/h3') else "No Product Details",
                "Pack Details": li.find_element(By.XPATH, './/span[contains(@class, "PackSelector___StyledLabel-sc-1lmu4hv-0")]').text if li.find_elements(By.XPATH, './/span[contains(@class, "PackSelector___StyledLabel-sc-1lmu4hv-0")]') else "No Pack Details",
                "Discounted Price": li.find_element(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel-sc-pldi2d-1")]').text if li.find_elements(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel-sc-pldi2d-1")]') else "No Discounted Price",
                "Original Price": li.find_element(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel2-sc-pldi2d-2")]').text if li.find_elements(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel2-sc-pldi2d-2")]') else "No Original Price"
            }
            products_data.append(product_data)
        except Exception as e:
            logging.warning(f"Error extracting product data: {e}")
    
    return products_data


def main():
    driver = launch_browser()
    try:
        categories = extract_categories(driver)
        
        if categories:
            for category in categories:  
                category_name = category["name"].replace(" ", "_")
                category_link = category["link"]
                logging.info(f"Processing category: {category_name}")
                
                products = scrape_category_items(driver, category_link)
                
                if products:
                    save_to_csv(products, f"{category_name}_products.csv")
                    save_to_json(products, f"{category_name}_products.json")
                else:
                    logging.warning(f"No products found for {category_name}")
        else:
            logging.error("No categories extracted.")
    except Exception as e:
        logging.error(f"Scraping process failed: {e}")
    finally:
        driver.quit()
        
        
        
def save_to_csv(data, filename):
    """Save data to CSV file."""
    try:
        if not data:
            logging.warning("No data to save in CSV.")
            return
        
        keys = data[0].keys()
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"CSV save error: {e}")


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



if __name__ == "__main__":
    main()