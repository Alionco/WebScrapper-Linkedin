from cmath import exp
from lib2to3.pgen2.token import OP
from bs4 import BeautifulSoup #usado para parsear conteudo html

#selenium e o webdriver são usados para carregar paginas e fazer requisicoes
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options #importa opcoes de inicializacao do firefox
from selenium.webdriver.firefox.service import Service #importa opcoes de inicializacao do firefox

import json


import os #usado para pegar as variaveis de ambiente
from dotenv import load_dotenv #usado para carregar variaveis de ambiente

load_dotenv()

options = Options()
#options.headless = True #usado para deixar de abrir uma pagina de verdade

#é necessário baixar o geckodriver, deixar ele no root do projeto com chmod +x e indicar o path dele aqui
#webdriver é pagina que vai ser aberta, carregada, ter dados extraidos, etc
service = Service("./geckodriver")
driver = webdriver.Firefox(service=service)
driver.get("https://linkedin.com/uas/login/")

#encontra as tags do HTML por ID
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

#simula a inserção de texto com base nas variaveis de ambiente
username.send_keys(LINKEDIN_USER)  
password.send_keys(LINKEDIN_PASSWORD)

#encontra a tag HTML do botão de login através de XPATH
#pode ser encontrada inspecionando a pagina e copiando o XPATH dela
# Format (syntax) of writing XPath --> 
# //tagname[@attribute='value']
loginButton = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button")
loginButton.click()

driver.get("https://www.linkedin.com/in/lucas-alionco/")

#scroll para o fim da pagina - CUIDADO, se a pagina for infinita, precisa usar uma logica para apertar o botao de novo quando vc quiser...
#se nao der scroll na pagina, alguns dados que so aparecem quando se chega ao fim da pagina nao conseguem ser capturados

pagina = driver.find_element(By.TAG_NAME, "html")
pagina.send_keys(Keys.END)

#monta a estrutura do objeto final que desejamos construir
data = {
    "status_age": "",
    "name": "",
    "last_query":"",
    "activity_linkedin":""
}

#encontra o elemento que tem o dado desejado, pega seu texto e coloca no campo do objeto
name = driver.find_element(By.XPATH,"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1").text
data["name"] = name

activity = driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]").text
data["activity_linkedin"] = activity

#about = driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]").text



print(json.dumps(data))

#fecha a pagina
driver.quit()
