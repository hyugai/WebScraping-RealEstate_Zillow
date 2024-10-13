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
        chrome_options.add_argument("--headless")
        
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(self.homepage_url)
        time.sleep(3)

    def start(self) -> None:
        self._set_up()

    def return_homepage(self) -> None:
        self.browser.get(self.homepage_url)

    def quit(self) -> None:
        self.browser.quit()