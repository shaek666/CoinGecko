# Import necessary libraries
from selenium import webdriver  # For controlling the web browser
from selenium.webdriver.chrome.service import Service  # Manages ChromeDriver service
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  # Helps in waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC  # Defines conditions for waiting
from selenium.common.exceptions import NoSuchElementException  # Handles missing elements
import pandas as pd  
import time  

# Configuration variables
BASE_URL = "https://www.coingecko.com/"  
MAX_PAGES = 50  
CSV_FILENAME = "coingecko_data.csv"  

# Dictionary defining column indexes for extracting data from the webpage table
COLUMN_MAP = {
    "Coin": 2,  
    "Price": 4,  
    "1h": 5,  
    "24h": 6,  
    "7d": 7,  
    "24h Volume": 9,  
    "Market Cap": 10 
}

def setup_driver():
    
    chrome_options = Options()
    # Prevents detection as a bot
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Sets a user-agent string to mimic a normal web browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    
    service = Service(executable_path=r"F:\chromedriver-win64 (1)\chromedriver.exe")
    
    # Return the initialized WebDriver instance
    return webdriver.Chrome(service=service, options=chrome_options)

def handle_popups(driver):
    try:
        # Waits for the "Got it" button of the cookie pop up to be clickable and clicks it
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Got it')]")
        )).click()
    except:
        pass  # Ignore if the popup does not appear

def scrape_page(driver):
    try:
        # Waits until the page table with "Market Cap" header is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table//th[contains(., 'Market Cap')]"))
        )
        
        # Find all table rows in the body of the table
        rows = driver.find_elements(By.XPATH, "//tbody/tr")
        page_data = []  # List to store extracted data
        
        for row in rows:
            try:
                # Find all table cells within the row
                cells = row.find_elements(By.TAG_NAME, "td")
                
                # Skip row if it does not contain enough columns
                if len(cells) < max(COLUMN_MAP.values()):
                    continue
                    
                # Extract relevant data based on COLUMN_MAP and clean up text
                entry = {
                    "Coin": cells[COLUMN_MAP["Coin"]].text.strip(),
                    "Price": cells[COLUMN_MAP["Price"]].text.replace("$", "").strip(),
                    "1h": cells[COLUMN_MAP["1h"]].text.replace("%", "").strip(),
                    "24h": cells[COLUMN_MAP["24h"]].text.replace("%", "").strip(),
                    "7d": cells[COLUMN_MAP["7d"]].text.replace("%", "").strip(),
                    "24h Volume": cells[COLUMN_MAP["24h Volume"]].text.replace("$", "").strip(),
                    "Market Cap": cells[COLUMN_MAP["Market Cap"]].text.replace("$", "").strip()
                }
                page_data.append(entry)
                
            except Exception as e:
                print(f"Error processing row: {str(e)}")  # Print error if row processing fails
                continue
                
        return page_data
        
    except Exception as e:
        print(f"Page scraping failed: {str(e)}")  # Print error if scraping fails
        return []  # Return an empty list

def main():
    
    driver = setup_driver()  # Initialize the Selenium WebDriver
    all_data = []  
    
    try:
        # Loop through multiple pages up to MAX_PAGES
        for page_num in range(1, MAX_PAGES + 1):
            try:
                # Construct the page URL
                url = BASE_URL if page_num == 1 else f"{BASE_URL}?page={page_num}"
                print(f"Processing page {page_num}: {url}")
                
                driver.get(url)
                handle_popups(driver)
                time.sleep(2)
                
                # Check if the page returned a 404 error (page not found)
                if "404" in driver.title:
                    print(f"Page {page_num} not found, stopping")
                    break  # Stop scraping if a page does not exist
                
                # Scrape data from the current page
                data = scrape_page(driver)
                
                # If no data is found, stop scraping further pages
                if not data:
                    print(f"No data found on page {page_num}, stopping")
                    break
                
                all_data.extend(data)  # Add the extracted data to the main list
                print(f"Collected {len(data)} records from page {page_num}")
                
            except Exception as e:
                print(f"Error on page {page_num}: {str(e)}")
                continue  # Continue to the next page if an error occurs

        if all_data:
            df = pd.DataFrame.from_records(all_data)
            
            # Convert numerical columns from string to numeric type
            numeric_cols = ['Price', '1h', '24h', '7d', '24h Volume', 'Market Cap']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
            
            df.to_csv(CSV_FILENAME, index=False)  # Save data to CSV
            print(f"\nSuccessfully saved {len(df)} records to {CSV_FILENAME}")

        else:
            print("No data collected")

    finally:
        driver.quit()
        print("Scraping completed!")

if __name__ == "__main__":
    main()