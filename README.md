# Cheap Mart - Online Grocery Price Comparison Platform

## Overview
**Cheap Mart** is an online platform that helps users compare grocery prices across multiple e-grocery stores such as **Zepto, Swiggy Instamart, BigBasket, Blinkit, and Koyambedu Market**. Users can search for products, view prices from different stores, compare discounts, and get direct links to purchase.

## Features
### 🔍 Product Search & Comparison
- Search for grocery items and view **prices from different stores**.
- Compare prices, discounts, and availability in **real time**.
- Direct links to purchase products from the respective stores.

### 🛒 Smart Shopping Experience
- **Filter by categories** (Fruits, Vegetables, Dairy, Snacks, Beverages, Household, Personal Care, etc.).
- Sort by **price, discount, popularity**.
- **Wishlist & Cart** to save and compare products.
- Smart cart optimization to suggest the **cheapest store** for all selected items.

### 📊 Product Detail Page
- Expanded product details including **brand, pack size, description, and nutrition facts**.
- **Comparison table** showing price, discounts, and purchase links from different stores.

### 📌 User Account & Personalization
- User authentication with **Google/email login**.
- **Saved preferences**, frequently searched items.
- **Order history tracking & price alerts**.

### 📱 Mobile-Friendly UI
- **Fully responsive design** for mobile, tablet, and desktop.
- **Modern and intuitive UI** with clean navigation and easy product browsing.

## Tech Stack
### 🌐 Frontend
- **React.js** with Tailwind CSS for a modern UI.
- State management using **Redux**.
- **Axios** for fetching price comparison data from APIs.

### ⚙️ Backend
- **Node.js** with **Express.js** for API development.
- **MongoDB/PostgreSQL** for storing product and pricing data.
- **Scrapy + Playwright/Puppeteer** for web scraping e-grocery store prices.

### 🔗 APIs & Integrations
- Store price fetching using **scraping & APIs**.
- Google Firebase for **user authentication**.
- Deployment using **Vercel/Netlify** for frontend and **Render/Heroku** for backend.

## Installation & Setup
### 🛠 Prerequisites
- Node.js & npm
- MongoDB/PostgreSQL
- Python (for Scrapy)

### 🚀 Steps to Run Locally
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/cheap-mart.git
   cd cheap-mart
   ```

2. **Install frontend dependencies**
   ```sh
   cd frontend
   npm install
   npm start
   ```

3. **Install backend dependencies**
   ```sh
   cd backend
   npm install
   npm start
   ```

4. **Run the scraper (for fetching prices)**
   ```sh
   cd scraper
   python scraper.py
   ```

## Roadmap
- [ ] Implement **automated price updates**.
- [ ] Add **store-specific filtering & sorting**.
- [ ] Create a **browser extension** for quick price lookup.
- [ ] Introduce **AI-based personalized price suggestions**.

## Contribution
We welcome contributions! Please open an issue or submit a pull request.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Contact
For any queries, feel free to reach out:
📧 Email: thanigaivelan2004@gmail.com
## UI Deign
<img src="./UI Design/Landing Page.jpg">
<img src="./UI Design/Product Detail Page.jpg">
<img src="./UI Design/Product Listing Page.jpg">
