# libs
from _libs import *
from _usr_libs import *

# class Zillow headless browser mode
class ZillowHeadlessBrowser():
    def __init__(self) -> None:
        self.homepage_url = "https://www.zillow.com/"
        self.user_agent = USER_AGENT

    def _set_up(self) -> None:
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"user-agent={self.user_agent}")
        #chrome_options.add_argument("--headless")
        
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(self.homepage_url)
        time.sleep(3)

    def start(self) -> None:
        self._set_up()

    def find_element(self, xpath: str) -> WebElement:
        return self.browser.find_element(By.XPATH, xpath)

    def find_elements(self, xpath: str) -> list[WebElement]:
        return self.browser.find_elements(xpath)