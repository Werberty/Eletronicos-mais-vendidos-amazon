from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# Caminho para a raiz do projeto
ROOT_FOLDER = Path(__file__).parent.parent.parent
# Caminho para a pasta onde o chromedriver está
CHROME_DRIVER_PATH = ROOT_FOLDER / 'bin' / 'chromedriver'


class BrowserChrome:
    def __init__(self, *options) -> None:
        self.chrome_options = webdriver.ChromeOptions()

        if options is not None:
            for option in options:
                self.chrome_options.add_argument(option)

        self.chrome_service = Service(
            executable_path=CHROME_DRIVER_PATH,
        )

        self.browser = webdriver.Chrome(
            service=self.chrome_service,
            options=self.chrome_options
        )

    def acessa(self, link):
        self.browser.get(link)

    def sair(self):
        self.browser.quit()


if __name__ == '__main__':
    drive = BrowserChrome('--disable-gpu', '--no-sandbox')
    drive.acessa('https://www.amazon.com.br/gp/bestsellers/electronics')
    sleep(4)
    drive.sair()
