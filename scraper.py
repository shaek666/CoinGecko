# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd  
import time  


BASE_URL = "https://www.coingecko.com/"  
MAX_PAGES = 50  
CSV_FILENAME = "coingecko_data.csv"  


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
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    
    service = Service(executable_path=r"F:\chromedriver-win64 (1)\chromedriver.exe")
    
    
    return webdriver.Chrome(service=service, options=chrome_options)

def handle_popups(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Got it')]")
        )).click()
    except:
        pass

def scrape_page(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table//th[contains(., 'Market Cap')]"))
        )
        
        rows = driver.find_elements(By.XPATH, "//tbody/tr")
        page_data = []
        
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) < max(COLUMN_MAP.values()):
                    continue
                    
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
                print(f"Error processing row: {str(e)}")
                continue
                
        return page_data
        
    except Exception as e:
        print(f"Page scraping failed: {str(e)}")
        return []

def main():
    
    driver = setup_driver()
    all_data = []  
    
    try:
        for page_num in range(1, MAX_PAGES + 1):
            try:
                url = BASE_URL if page_num == 1 else f"{BASE_URL}?page={page_num}"
                print(f"Processing page {page_num}: {url}")
                
                driver.get(url)
                handle_popups(driver)
                time.sleep(2)
                
                if "404" in driver.title:
                    print(f"Page {page_num} not found, stopping")
                    break
                
                data = scrape_page(driver)
                
                if not data:
                    print(f"No data found on page {page_num}, stopping")
                    break
                
                all_data.extend(data) 
                print(f"Collected {len(data)} records from page {page_num}")
                
            except Exception as e:
                print(f"Error on page {page_num}: {str(e)}")
                continue  

        if all_data:
            df = pd.DataFrame.from_records(all_data)
            
            numeric_cols = ['Price', '1h', '24h', '7d', '24h Volume', 'Market Cap']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
            
            df.to_csv(CSV_FILENAME, index=False)
            print(f"\nSuccessfully saved {len(df)} records to {CSV_FILENAME}")

        else:
            print("No data collected")

    finally:
        driver.quit()
        print("Scraping completed!")

if __name__ == "__main__":
    main()