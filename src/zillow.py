# libs
from _libs import *
from _usr_libs import *

# class Zillow headless browser mode
class ZillowHeadlessBrowser():
    def __init__(self, 
                 headers: dict) -> None:
        self.homepage_url = "https://www.zillow.com/"
        self.headers = headers
        self.user_agent = USER_AGENT

    def _set_up(self) -> None:
        chrome_options = ChromeOptions()
        for key, value in self.headers.items():
            chrome_options.add_argument(f"{key}={value}")
        #chrome_options.add_argument("--headless")
        # chrome_options.add_experimental_option("detach", True)
        
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(self.homepage_url)

    def start(self) -> None:
        self._set_up()

    def find_element(self, xpath: str) -> WebElement:
        return self.browser.find_element(By.XPATH, xpath)

    def find_elements(self, xpath: str) -> list[WebElement]:
        return self.browser.find_elements(xpath)