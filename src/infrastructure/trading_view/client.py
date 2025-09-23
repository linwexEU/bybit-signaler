import pickle
import time
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from src.domain.interfaces import AbstractTradingView
from src.config import settings


class TradingView(AbstractTradingView): 
    LOGIN_URL: str = "https://ru.tradingview.com/pricing/?source=promo_go_pro_button#"

    def __init__(self): 
        # Init options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("prefs", {
            "profile.content_settings.exceptions.clipboard": {
                "[*.],*": {
                    "last_modified": "1576491240619",
                    "setting": 1
                }
            }
        })
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": settings.DOWNLOAD_DIR,  
            "download.prompt_for_download": False,       
            "download.directory_upgrade": True,         
            "safebrowsing.enabled": True            
        })

        self.driver = webdriver.Chrome(options=chrome_options)

    def _save_login_cookies(self) -> None: 
        pickle.dump(self.driver.get_cookies(), open(fr"{settings.COOKIES_PATH}\tw_cookies", "wb")) 

    def _load_login_cookies(self) -> None: 
        for cookie in pickle.load(open(fr"{settings.COOKIES_PATH}\tw_cookies", "rb")): 
            self.driver.add_cookie(cookie)
        time.sleep(1)

        # Load driver with cookies
        self.driver.refresh()

    def _wait_until_page_loaded(self) -> None: 
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _wait_for_element(self, element: tuple) -> None: 
        while True: 
            try: 
                WebDriverWait(self.driver, 15).until(
                    EC.visibility_of(self.driver.find_element(element[0], element[1]))
                )
                break 
            except: 
                continue

    def login_without_automation(self, time_to_wait: int = 200) -> None:
        self.driver.get(self.LOGIN_URL)
        self._wait_until_page_loaded()

        # Your time for registration
        time.sleep(time_to_wait)

        # Save cookies
        self._save_login_cookies()

    def _download_screenshot(self) -> None: 
        screenshot_button = self.driver.find_element(By.XPATH, '//*[@id="header-toolbar-screenshot"]')
        screenshot_button.click() 
        time.sleep(1)

        download_screenshot = self.driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div[2]/span/div[1]/div/div/div[2]')
        download_screenshot.click()
        time.sleep(1)

    def _open_additional_tfs(self) -> None:
        additional_tf = self.driver.find_element(By.XPATH, '//*[@id="header-toolbar-intervals"]/button')
        additional_tf.click()
        time.sleep(1)

    def get_ticker_chart(self, ticker: str) -> None: 
        self.driver.get("https://ru.tradingview.com/")
        self._load_login_cookies()
        self._wait_until_page_loaded()

        # Set size for headless mode
        self.driver.set_window_size(1920, 1080)

        # Search button
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/div/button[1]')
        search_button.click()

        # Input form
        input_form = self.driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/span/form/input')
        input_form.send_keys(ticker.upper())
        time.sleep(1)

        # Press to first ticker
        first_ticker = self.driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[1]/div[2]')
        first_ticker.click()
        
        # Wait our element
        self._wait_for_element((By.XPATH, '//*[@id="header-toolbar-screenshot"]'))
        time.sleep(1)

        # 1h TF
        self._download_screenshot()

        # 5m TF
        tf_5m_button = self.driver.find_element(By.XPATH, '//*[@id="header-toolbar-intervals"]/div/button[1]')
        tf_5m_button.click()
        time.sleep(1)

        self._download_screenshot()

        # 15m TF
        tf_15m_button = self.driver.find_element(By.XPATH, '//*[@id="header-toolbar-intervals"]/div/button[2]')
        tf_15m_button.click()
        time.sleep(1)

        self._download_screenshot()

        # 4h TF
        tf_14h_button = self.driver.find_element(By.XPATH, '//*[@id="header-toolbar-intervals"]/div/button[4]')
        tf_14h_button.click()
        time.sleep(1)

        self._download_screenshot()

        # Open additional TF
        self._open_additional_tfs()

        # 1D TF 
        tf_1d_button = self.driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div[2]/span/div[1]/div/div/div/div[34]/div')
        tf_1d_button.click()
        time.sleep(1)

        self._download_screenshot()

        # Open additional TF
        self._open_additional_tfs()

        # 1W TF
        tf_1w_button = self.driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div[2]/span/div[1]/div/div/div/div[36]/div')
        tf_1w_button.click()
        time.sleep(1)

        self._download_screenshot()

    def close_driver(self) -> None: 
        self.driver.close() 
        self.driver.quit() 

    def __enter__(self) -> "TradingView": 
        return self
    
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: 
        self.close_driver()
