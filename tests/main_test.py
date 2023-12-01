import time
import re
import pandas as pd
import pyautogui
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller


class Pesquisa:
    def __init__(self):
        # Inicialização do webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
          "download.default_directory": r"C:\Users\miguel.silva",
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        self.tribunais_sites = {
            # Armazena as URL dos códigos de processo
            8.26: "https://esaj.tjsp.jus.br/cjpg/",
            8.19: "https://www.tjrj.jus.br/",
        }
        
        self.df = None
        self.df = pd.read_excel('dados_processo_final v.0111.xlsx')
        
        
    def obter_url_por_numero_tribunal(self, numero_tribunal):
        if numero_tribunal in self.tribunais_sites:
            return self.tribunais_sites[numero_tribunal]
        else:
            return None
        
        
    def extrair_numero_tribunal(self, numero_processo):
        padrao = r'\.(\d+\.\d+)\.'  # Expressão regular para encontrar o padrão 'número.número'
        resultado = re.search(padrao, numero_processo)
        
        if resultado:
            return resultado.group(1)  # Retorna o número do tribunal encontrado
        else:
            return None
        
        if resultado: 
            return resultado.group(2)
        else: 
            return None
    
    def acessar_sites(self):
        
        for index, row in df.iterrows():
        
            if resultado:
                numero_tribunal = resultado.group(0)
                print(f"Número do tribunal encontrado para o processo {numero_processo}: {numero_tribunal}")
            else:
                print(f"Número do tribunal não encontrado para o processo {numero_processo}.")
                
            if resultado:
                numero_tribunal = resultado.group(1)
                print(f"Número do tribunal encontrado para o processo {numero_processo}: {numero_tribunal}")
            else:
                print(f"Número do tribunal não encontrado para o processo {numero_processo}.")