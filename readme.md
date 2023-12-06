# Processamento de Dados Judiciais

Este script Python foi desenvolvido para automatizar o processo de consulta e processamento de informações judiciais em sites específicos de tribunais. Ele usa a biblioteca Selenium para interagir com os elementos da página web e o PyAutoGUI para simular interações de mouse e teclado.

## Pré-requisitos

Certifique-se de ter instalado os seguintes componentes antes de executar este script:

- Python 3.x
- Bibliotecas Python: pandas, pyautogui, navegador, selenium, chromedriver_autoinstaller

## Instalação das Dependências

```bash
pip install pandas pyautogui selenium chromedriver_autoinstaller
```

# Uso
1. Iniciando o Script:

- Execute o script Python para automatizar a consulta e processamento dos dados judiciais. Certifique-se de ter conexão com a internet durante a execução.

2. Funcionamento:

- O script lê um arquivo Excel existente, dados_processo_final v.0111.xlsx, contendo informações de processos judiciais.
- Itera pelos processos e realiza consultas nos sites dos tribunais configurados (esaj.tjsp.jus.br e www3.tjrj.jus.br) usando Selenium.
- Extrai informações dos processos dentro do intervalo de anos de 2019 a 2023.
- Realiza ações automatizadas de preenchimento de campos, cliques em botões e salvamento de documentos PDF.
- Atualiza o status dos processos no arquivo Excel dados_processo_final.xlsx após o processamento.

# Notas Adicionais
- É necessário configurar o tempo de espera e os locais dos elementos na página conforme necessário para evitar erros de tempo limite.
- Certifique-se de adicionar outros tribunais na classe Pesquisa se desejar expandir a funcionalidade para mais locais.

# Observações
- Este código está sujeito a mudanças e personalizações, especialmente nas partes relacionadas ao Selenium, conforme a estrutura do site do tribunal.