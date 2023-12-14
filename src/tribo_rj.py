import time
import pandas as pd
import pyautogui
import requests
from navegador import Navegador
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

class ProcessadorDeProcessos:
    def __init__(self, driver):
        self.driver = driver
        
class Pesquisa:
    def __init__(self):
        self.tribunais_sites = {
            8.19: 'https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS',
            # Adicione outros tribunais aqui
        }

def main():
  navegador = Navegador()
  driver = navegador.iniciar_chrome()
  
  navegador.driver.get('https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS')
  navegador.driver.find_element(By.XPATH, '//*[@id="iniciodoconteudo"]/div[1]/form/div/div[2]/div/div[2]/div/div/div[2]/a').click()
  janelas_abertas = navegador.driver.window_handles

  navegador.driver.switch_to(janelas_abertas[1])
  wait = WebDriverWait(navegador.driver, 20)
  input_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dropdownPerfil"]/div/div[1]/div[1]/input')))
  input_element.send_keys('Advogado')
  pyautogui.press('enter')
  time.sleep(0.7)
  navegador.driver.execute_script("javascript:void(0)")
  print("Usuário Logado")
  time.sleep(5)


  # Ações antes da consulta de processos, necessário fazer scrap na página
  navegador.driver.find_element(By.XPATH, '//*[@id="PORTLET"]').click()
  consulta_intimacao = WebDriverWait(navegador.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[4]/div')))
  consulta_intimacao.click()
  time.sleep(2)
  input_place = WebDriverWait(navegador.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="filtroStatus"]')))
  input_place.send_keys('Recebidas', Keys.ARROW_DOWN)
  pyautogui.press('enter')
  time.sleep(2)

  navegador.driver.find_element(By.XPATH, '//*[@id="botaoPesquisarIntimacoes"]').click()

  # scrap
  response = requests.get(site_rj)
  if response.status_code == 200:
      html_content = response.txt
      
      soup = BeautifulSoup(html_content, 'html.parser')
      
      processo_element = soup.select("(//td[contains(@class,'ng-tns-c405-2')])[3]")
      
      for element in processo_element:
          text = element.get_text(strip=True)
          print(f"Numero Processo: {text}")
  else:
      print('Falha ao processar página: ', response.status_code)

  # Consultar processo
  navegador.driver.find_element(By.XPATH, '//*[@id="CONSULTAS"]').click()
  consulta_processo = WebDriverWait(navegador.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[1]/div')))
  consulta_processo.click()
  
if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Error: {e}")