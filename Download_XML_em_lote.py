from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#cria opção headless do firefox
options = Options()
options.add_argument("--headless")
#abre csv com chaves a serem baixadas
chaves=pd.read_csv(r"C:\XML-059078220020-37\112022\chaves.csv",sep=";",encoding="UTF-8")
#contador com quantidade de chaves menos uma (indice inicia em zero)
i=len(chaves)-1
#cria lista para salvar chaves
chavexml=[]
#laço para incrementar chaves à lista
while i>=0:
    chavexml.append(chaves.iloc[i]['CHAVE'])
    i-=1
#Novo contador para pesquisar chaves
i=len(chavexml)-1
#Abre instância do navegador
sitedanfe=webdriver.Firefox(options=options)

#Laço para percorrer lista de chaves 
while i>=0:
    #try except para pegar erros
    try: 
        #Aguarda resposta do site
        print("Aguardando resposta do site")
        wait = WebDriverWait(sitedanfe, 120)
        
        sitedanfe.get('https://meudanfe.com.br/')
        wait.until(EC.element_to_be_clickable(sitedanfe.find_element(By.ID,"chaveAcessoBusca")))
        #Acha campo de enviar chaves e envia chave na posição i da lista
        chave= sitedanfe.find_element(By.ID,"chaveAcessoBusca")
        chave.send_keys(chavexml[i])
        print("pesquisando chave")
        #encontra e clica no botão de consultar
        wait.until(EC.element_to_be_clickable(sitedanfe.find_element(By.CLASS_NAME,"btn.btn-success.btn-round")))
        consultar=sitedanfe.find_element(By.CLASS_NAME,"btn.btn-success.btn-round")
        
        consultar.click()
        #encontra botão de baixar xml e clica para iniciar download
        wait.until(EC.element_to_be_clickable(sitedanfe.find_element(By.CLASS_NAME,"btn.btn-warning.btn-round.btn-lg.btn-block")))
        baixarxml=sitedanfe.find_element(By.CLASS_NAME,"btn.btn-warning.btn-round.btn-lg.btn-block")
        print(("baixando XML"))
        baixarxml.click()

        print(f"Baixado arquivo {i}")
        #decrementa contador
        i-=1
        
    #except com erro, fechamento e reabertura de navegador
    except Exception as E:
        print("Tentando novamente \n",E)
        sitedanfe.quit()
        sitedanfe=webdriver.Firefox(options=options)
        