from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
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

    def raspa_dados_dos_produtos(self):
        lista_dados_produtos = {}
        try:
            lista_produtos = self.obter_lista_produtos()
            for n, produto in enumerate(lista_produtos):
                titulo = produto.select(
                    '#gridItemRoot > div > div.zg-grid-general-faceout > div > a:nth-child(2) > span > div'
                )[0].get_text()

                preco = produto.select(
                    '#gridItemRoot > div > div.zg-grid-general-faceout > div > div:nth-child(4) > a > span > span'
                )[0].get_text()

                link = 'https://www.amazon.com.br' + produto.select_one(
                    '#gridItemRoot > div > div.zg-grid-general-faceout > div > a:nth-child(2)'
                ).get('href')
                print(link, '\n')

                lista_dados_produtos[f'#{n+1}'] = {'Titulo': titulo, 'Preco': preco}
                # titulo = self.limpar_titulo(titulo)
        except Exception as e:
            print('ERRO:', e)

        # print(lista_dados_produtos)
    
    def obter_lista_produtos(self):
        self.rolar_pagina()
        html_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        lista_produtos = html_soup.select('#gridItemRoot > div')
        return lista_produtos
    
    def limpar_titulo(self, titulo):
        if ':' in titulo:
            titulo = titulo.split(':')[0]
        if '-' in titulo:
            titulo = titulo.split('-')[0]
        if '|' in titulo:
            titulo = titulo.split('|')[0]
        if '–' in titulo:
            titulo = titulo.split('–')[0]

        return titulo
        
    def rolar_pagina(self):
        page = self.browser.find_element(By.TAG_NAME, 'html')
        page.send_keys(Keys.END)
        sleep(4)

    def acessa(self, link):
        self.browser.get(link)

    def sair(self):
        self.browser.quit()


if __name__ == '__main__':
    drive = BrowserChrome('--disable-gpu', '--no-sandbox')
    drive.acessa('https://www.amazon.com.br/gp/bestsellers/electronics')
    drive.raspa_dados_dos_produtos()
    sleep(4)
    drive.sair()
