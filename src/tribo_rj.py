import time
import requests
import pyautogui
import sqlite3
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
    
    @staticmethod
    def salvar_numeros_processo_no_sqlite(numeros_processo):
        conn = sqlite3.connect('numeros_processo.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS numeros_processo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            numero_processo TEXT
                        )''')

        for numero in numeros_processo:
            cursor.execute("INSERT INTO numeros_processo (numero_processo) VALUES (?)", (numero,))

        conn.commit()
        conn.close()
    
    def verificar_processos_salvos(self, numeros_processo):
        conn = sqlite3.connect('numeros_processo.db')
        cursor = conn.cursor()

        cursor.execute("SELECT numero_processo FROM numeros_processo")
        numeros_salvos = cursor.fetchall()
        numeros_salvos = [numero[0] for numero in numeros_salvos]

        conn.close()

        return set(numeros_processo) == set(numeros_salvos)
    
    
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
                time.sleep(8)
                
                wait = WebDriverWait(navegador.driver, 20)
                element_arrow = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"form-group botao-dropdown")]')))
                element_arrow.click()
                time.sleep(7)
                
                input_element = wait.until(EC.presence_of_element_located((By.XPATH, "(//li[contains(@role,'option')])[2]")))
                input_element.click()
                
                
                time.sleep(5)
                botao = navegador.driver.find_element(By.XPATH, "//div[@class='rodape-confirma'][contains(.,'Entrar')]")
                botao.click()
                # botao.execute_script("javascript:void(0)")
                
                print("Usuário Logado")
                time.sleep(5)
                
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
                print(f"Error: {e}")
                
    
   
    
    def consultar_intimacoes(self):
        # code for consulting intimacoes
        navegador.driver.find_element(By.XPATH, "//li[contains(@id,'PORTLET')]").click()
        consulta_intimacao = WebDriverWait(navegador.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button'][contains(.,'Intimações / Citações Eletrônicas Intimações / Citações Eletrônicas')]")))
        consulta_intimacao.click()
        time.sleep(2)
        input_place = WebDriverWait(navegador.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="filtroStatus"]')))
        input_place.clear()
        time.sleep(0.7)
        input_place.send_keys('Recebidas', Keys.ARROW_DOWN)
        pyautogui.press('enter')
        time.sleep(2)

        navegador.driver.find_element(By.XPATH, '//*[@id="botaoPesquisarIntimacoes"]').click()
        
        # Scraping part
        site_scrap = 'https://www3.tjrj.jus.br/portalservicos/#/portlets/intimacoes-citacoes'
        response = requests.get(site_scrap)

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            elementos_td = soup.find_all('td', attrs={'aria-describedby': lambda x: x and 'tooltip732239' in x})
            
            numeros_processo = []
            for td in elementos_td:
                link_a = td.find('a', attrs={'class': 'texto-link ng-tns-c408-3'}) 
                if link_a:
                    numero_processo = link_a.get_text(strip=True)
                    numeros_processo.append(numero_processo)
            
            # Salvar os números de processo no banco de dados
            self.salvar_numeros_processo_no_sqlite(numeros_processo)
            print("Números de processo salvos com sucesso no banco de dados!")

            # Verificar se todos os números de processo foram salvos no banco de dados
            if self.verificar_processos_salvos(numeros_processo):
                print("Todos os números de processo foram salvos no banco de dados!")
            else:
                print("Alguns números de processo não foram salvos no banco de dados.")
        else:
            print('Failed to process page: ', response.status_code)

        # Chamada direta ao método consultar_processo
        # self.consultar_processo()
    
    
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

        
    except Exception as e:
        print(f"Error: {e} presented in process.")

if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Error: {e}")
