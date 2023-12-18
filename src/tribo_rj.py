import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from navegador import Navegador

navegador = Navegador()
driver = navegador.iniciar_chrome()

class ProcessadorDeProcessos:
    def __init__(self, driver):
        self.driver = driver
        
    def login(self):
        try:
            driver.get('https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS')
            try:
                login_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="iniciodoconteudo"]/div[1]/form/div/div[2]/div/div[2]/div/div/div[2]/a'))
                )
                login_button.click()
                janelas_abertas = self.driver.window_handles

                self.driver.switch_to(janelas_abertas[1])
                wait = WebDriverWait(self.driver, 20)
                input_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dropdownPerfil"]/div/div[1]/div[1]/input')))
                input_element.send_keys('Advogado')
                pyautogui.press('enter')
                time.sleep(0.7)
                self.driver.execute_script("javascript:void(0)")
                print("Usuário Logado")
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
                print(f"Error: {e}")
                
                
    def consultar_intimacoes(self):
        # code for consulting intimacoes
        self.driver.find_element(By.XPATH, '//*[@id="PORTLET"]').click()
        consulta_intimacao = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[4]/div')))
        consulta_intimacao.click()
        time.sleep(2)
        input_place = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="filtroStatus"]')))
        input_place.send_keys('Recebidas', Keys.ARROW_DOWN)
        pyautogui.press('enter')
        time.sleep(2)

        self.driver.find_element(By.XPATH, '//*[@id="botaoPesquisarIntimacoes"]').click()
        

    def consultar_processo(self):
        # code for consulting processo
        self.driver.find_element(By.XPATH, '//*[@id="CONSULTAS"]').click()
        consulta_processo = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[1]/div')))
        consulta_processo.click()
        
        
class Pesquisa:
    def __init__(self):
        self.tribunais_sites = {
            8.19: 'https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS',
            # Add other tribunais here
        }

def main():
    processador = ProcessadorDeProcessos(driver)
    pesquisa = Pesquisa()

    processador.login()
    processador.consultar_intimacoes()

    # Scraping part
    site_rj = 'https://www3.tjrj.jus.br/portalservicos/#/portlets/intimacoes-citacoes'
    response = requests.get(site_rj)
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        processo_element = soup.select("(//td[contains(@class,'ng-tns-c405-2')])[3]")
        
        for element in processo_element:
            text = element.get_text(strip=True)
            print(f"Numero Processo: {text}")
    else:
        print('Failed to process page: ', response.status_code)

    processador.consultar_processo()

if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Error: {e}")
