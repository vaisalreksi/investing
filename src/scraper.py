import os
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import traceback

class CommodityScraper:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('INVESTING_URL')
        self.driver = None

    def _initialize_driver(self):
        options = uc.ChromeOptions()

        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = uc.Chrome(options=options, headless=True)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            print("Chromedriver initialized successfully in headless mode.")
        except Exception as e:
            print(f"Error initializing Chromedriver: {e}")
            self.driver = None
    def get_data(self):
        if not self.driver:
            self._initialize_driver()
            if not self.driver:
                return None

        try:
            print(f"Navigating to {self.url}")
            self.driver.get(self.url)

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'realtime-futures-table'))
            )

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            price_data = self._extract_price_data(soup)
            performance_data = self._extract_performance_data(soup)
            technical_data = self._extract_technical_data(soup)
            specifications_data = self._extract_specifications_data(soup)

            all_data = {
                **price_data,
                **performance_data,
                **technical_data,
                **specifications_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return all_data

        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def _extract_price_data(self, soup):
        data_dict = {}
        try:
            table = soup.find('table', {'id': 'realtime-futures-table'})
            if table:
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) > 1: 
                        commodity_name = cols[1].text.strip() 
                        current_price = cols[2].text.strip() 
                        data_dict[f'{commodity_name}_price'] = current_price
            return data_dict
        except Exception as e:
            print(f"Error extracting price data: {str(e)}")
            return {'price_data': None}

    def _extract_performance_data(self, soup):
        return {'performance_data': None}

    def _extract_technical_data(self, soup):
        return {'technical_data': None}

    def _extract_specifications_data(self, soup):
        return {'specifications_data': None}