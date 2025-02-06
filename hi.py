from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")

# Automatically manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the URL
url = 'https://www.bigbasket.com/cl/electronics/?nc=nb&page=2'  # Replace with the actual URL you're scraping
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="mt-5 grid gap-6 grid-cols-9"]/li')))

# List to hold all product data
products_data = []

# Extract the <li> elements using an appropriate XPath or CSS selector
li_elements = driver.find_elements(By.XPATH, '//ul[@class="mt-5 grid gap-6 grid-cols-9"]/li')

# Loop through the <li> elements and extract data
for li in li_elements:
    try:
        # Extract offer (e.g., "57% OFF")
        try:
            offer = li.find_element(By.XPATH, './/span[contains(text(),"OFF")]').text
        except:
            offer = "No Offer"
        
        # Extract company name (e.g., "Wonderchef")
        try:
            company_name = li.find_element(By.XPATH, './/span[contains(@class,"BrandName___StyledLabel2-sc-hssfrl-1")]').text
        except:
            company_name = "No Company Name"
        
        # Extract product details (e.g., "Nutri Blend Mixer Grinder & Blender")
        try:
            product_details = li.find_element(By.XPATH, './/h3').text
        except:
            product_details = "No Product Details"
        
        # Extract pack details (e.g., "1 pc")
        try:
            pack_details = li.find_element(By.XPATH, './/span[contains(@class, "PackSelector___StyledLabel-sc-1lmu4hv-0")]').text
        except:
            pack_details = "No Pack Details"
        
        # Extract discounted price (e.g., ₹1149)
        try:
            discounted_price = li.find_element(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel-sc-pldi2d-1")]').text
        except:
            discounted_price = "No Discounted Price"
        
        # Extract original price (e.g., ₹6499)
        try:
            original_price = li.find_element(By.XPATH, './/span[contains(@class,"Pricing___StyledLabel2-sc-pldi2d-2")]').text
        except:
            original_price = "No Original Price"
        
        # Save extracted data
        product_data = {
            "Offer": offer,
            "Company Name": company_name,
            "Product Details": product_details,
            "Pack Details": pack_details,
            "Discounted Price": discounted_price,
            "Original Price": original_price
        }
        
        products_data.append(product_data)

    except Exception as e:
        print(f"Error extracting data for a product: {e}")

# Write the data to a CSV file
csv_file = 'products_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Offer", "Company Name", "Product Details", "Pack Details", "Discounted Price", "Original Price"])
    writer.writeheader()
    for product in products_data:
        writer.writerow(product)

# Close the driver
driver.quit()

print(f"Data has been saved to {csv_file}")
