from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Navegador:
    def __init__(self):
        self.driver = None

    def iniciar_chrome(self):
        # Configurar as opções do Chrome (por exemplo, desabilitar notificações)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
          "download.default_directory": r"C:\Users\miguel.silva",
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        # Substitua o caminho abaixo pelo caminho real do perfil de usuário do Chrome com barras invertidas duplas
        user_data_dir = r'C:\Users\miguel.silva\AppData\Local\Google\Chrome\User Data\Profile 1'
        options.add_argument(f"user-data-dir={user_data_dir}")

        # Iniciar o Chrome
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def fechar_chrome(self):
        if self.driver:
            self.driver.quit()

# Se este arquivo for executado diretamente, inicie o Chrome
if __name__ == "__main__":
    navegador = Navegador()
    navegador.iniciar_chrome()
