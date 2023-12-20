import time
import requests
import pyautogui
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from navegador import Navegador

navegador = Navegador()
driver = navegador.iniciar_chrome()

class ProcessadorDeProcessos:
    def __init__(self, driver):
        self.driver = driver
        
    def login(self):
        try:
            navegador.driver.get('https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS')
            try:
                login_button = WebDriverWait(navegador.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="iniciodoconteudo"]/div[1]/form/div/div[2]/div/div[2]/div/div/div[2]/a'))
                )
                login_button.click()
                
                # Accept the confirmation (click OK)
                pyautogui.moveTo(801, 340, duration=0.7)
                pyautogui.click()
                
                time.sleep(10)
                
                # Obtenha todas as janelas
                handles = navegador.driver.window_handles
                
                # Alterne para a janela de pop-up
                for handle in handles:
                    if handle != navegador.driver.current_window_handle:
                        navegador.driver.switch_to.window(handle)
                        break
                print("Title of the pop-up window:", navegador.driver.title)

                
                wait = WebDriverWait(navegador.driver, 20)
                element_arrow = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="form-group botao-dropdown"]/i[@class="f0a fa-caret-down fa-lg"]')))
                element_arrow.click()
                time.sleep(0.7)
                
                input_element = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@role='option' and @id='itemAutocomplete1']")))
                input_element.click()
                
                
                time.sleep(2)
                navegador.driver.execute_script("javascript:void(0)")
                print("Usuário Logado")
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
                print(f"Error: {e}")
                
                
    def consultar_intimacoes(self):
        # code for consulting intimacoes
        navegador.driver.find_element(By.XPATH, '//*[@id="PORTLET"]').click()
        consulta_intimacao = WebDriverWait(navegador.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[4]/div')))
        consulta_intimacao.click()
        time.sleep(2)
        input_place = WebDriverWait(navegador.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="filtroStatus"]')))
        input_place.send_keys('Recebidas', Keys.ARROW_DOWN)
        pyautogui.press('enter')
        time.sleep(2)

        navegador.driver.find_element(By.XPATH, '//*[@id="botaoPesquisarIntimacoes"]').click()
        

    def consultar_processo(self):
        # code for consulting processo
        navegador.driver.find_element(By.XPATH, '//*[@id="CONSULTAS"]').click()
        consulta_processo = WebDriverWait(navegador.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="corpo"]/app-menu-expandido/section/div/div[2]/div[1]/div')))
        consulta_processo.click()
        
        
class Pesquisa:
    def __init__(self):
        self.tribunais_sites = {
            8.19: 'https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS',
            # Add other tribunais here
        }

def main():
    try:
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
    except Exception as e:
        print(f"Error: {e} presented in process.")

if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Error: {e}")
