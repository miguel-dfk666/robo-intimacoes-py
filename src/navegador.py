from selenium import webdriver

class Navegador:
    def __init__(self):
        self.driver = None

    def iniciar_chrome(self):
        # Configurar as opções do Chrome (por exemplo, desabilitar notificações)
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        # Substitua o caminho abaixo pelo caminho real do perfil de usuário do Chrome com barras invertidas duplas
        user_data_dir = r'C:\Users\miguel.silva\\AppData\Local\Google\Chrome\User Data\Profile 2'
        #options.add_argument(f"user-data-dir={user_data_dir}")

        # Iniciar o Chrome
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def fechar_chrome(self):
        if self.driver:
            self.driver.quit()

# Se este arquivo for executado diretamente, inicie o Chrome
if __name__ == "__main__":
    navegador = Navegador()
    navegador.iniciar_chrome()
