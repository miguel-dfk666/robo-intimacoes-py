import time
import pandas as pd
import pyautogui
from navegador import Navegador
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller

# Instalar ou atualizar automaticamente o ChromeDriver
chromedriver_autoinstaller.install()

class ProcessadorDeProcessos:
    def __init__(self, driver):
        self.driver = driver

    def extrai_ano(self, numero_processo):
        try:
            partes = numero_processo.split(".")
            ano = partes[1][:4]  # Extrai os primeiros quatro caracteres após o primeiro ponto
            return ano
        except IndexError:
            return "Formato inválido"

    def process_spreadsheet(self, data):
        numeros_processo = data['Número do Processo']
        for numero_processo in numeros_processo:
            ano_processo = self.extrai_ano(numero_processo)
            if '2019' <= ano_processo <= '2023':
                self.process_with_selenium(numero_processo)
            else:
                print(f"Pulando o processo {numero_processo} por estar fora do intervalo de anos desejado.")
    
    # Funções relacionadas ao Selenium devem ser movidas aqui.
    # Como o método process_with_selenium não foi fornecido no código original, você deve implementá-lo.


class Pesquisa:
    def __init__(self):
        self.tribunais_sites = {
            8.26: 'https://esaj.tjsp.jus.br/cjpg/',
            8.19: 'https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS',
            # Adicione outros tribunais aqui
        }


def main():
    # Inicialize o navegador
    navegador = Navegador()
    driver = navegador.iniciar_chrome()

    # Lê a planilha existente
    nome_da_planilha = 'dados_processo_final v.0111.xlsx'
    df = pd.read_excel(nome_da_planilha)
    df['Status'] = df['Status'].fillna('')  # Set default Status to empty
    df['Número do Processo'] = df['Número do Processo'].str.strip()


    processador = ProcessadorDeProcessos(driver)
    pesquisa = Pesquisa()

    site_sp = 'https://esaj.tjsp.jus.br/cjpg/'
    site_rj = 'https://www3.tjrj.jus.br/idserverjus-front/#/login?indGet=true&sgSist=PORTALSERVICOS'
                    
    if site_sp: 
        driver.get(site_sp)
        for index, row in df.iterrows():
            if row['Status'] == '':
                try:                
                    # Configure um tempo limite de espera (por exemplo, 10 segundos)
                    wait = WebDriverWait(driver, 10)
                    time.sleep(4)
                    campo_pesquisa1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="numeroDigitoAnoUnificado"]')))
                    campo_pesquisa1.clear()
                    
                    campo_pesquisa2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="foroNumeroUnificado"]')))
                    campo_pesquisa2.clear()
                    
                    time.sleep(0.5)
                    
                    numero_processo = row["Número do Processo"]
                    numero_processo = str(numero_processo) 
                    numero_processo_parte1 = numero_processo[:15]  # Primeiros 15 caracteres
                    numero_processo_parte2 = numero_processo[-4:]  # Últimos 4 caracteres

                    campo_pesquisa1.send_keys(numero_processo_parte1)
                    time.sleep(0.5)

                    campo_pesquisa2.send_keys(numero_processo_parte2)
                    time.sleep(0.5)
                    
                    bttn_confirm = driver.find_element(By.XPATH, '//*[@id="pbSubmit"]')
                    bttn_confirm.click()
                    time.sleep(0.7)                
                

                            
                    # Clique no botão que abre a nova janela
                    try:
                        bttn_pdf = driver.find_element(By.XPATH, "//img[@title='Visualizar Inteiro Teor']")
                        bttn_pdf.click()
                        time.sleep(5)
                        # Define a posição onde deseja clicar
                        x_position = 427
                        y_position = 393

                        # Clique na posição
                        pyautogui.click(x_position, y_position)
                        
                        # element_download.click()
                        time.sleep(2)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(3)

                        pyautogui.hotkey('alt', 'f4')
                        driver.switch_to.window(driver.window_handles[0])

                        bttn2_confirm = driver.find_element(By.XPATH, '//*[@id="pbLimpar"]')
                        bttn2_confirm.click()   
                        time.sleep(0.7)
                        df.at[index, 'Status'] = 'ok'
                        # Exporte o DataFrame para uma planilha (fora do loop)
                        df.to_excel('dados_processo_final.xlsx', index=False)
                    except Exception as e:
                        logger.error(f"Erro desconhecido: {e}")
                        df.at[index, 'Status'] = 'Erro desconhecido'
                        continue
                except Exception as e:
                    print(f"Error: {e}")
                    
                # Exporte o DataFrame para uma planilha (fora do loop)
                df.to_excel('dados_processo_final.xlsx', index=False)
        
            #  Crie um DataFrame pandas com os dados coletados (fora do loop)
            # df = pd.DataFrame(dados_processos)
    elif site_rj:
        driver.get(site_rj)
        driver.find_element(By.XPATH, '//*[@id="iniciodoconteudo"]/div[1]/form/div/div[2]/div/div[2]/div/div/div[2]/a').click()
            
        


        
if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Error: {e}")
        
