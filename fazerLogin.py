from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()

def iniciar_navegador():
    chrome_options = Options()
    # Remove logs de erro do sistema do Chrome (como GCM, TensorFlow, etc)
    chrome_options.add_argument('--log-level=3') 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    return driver

def fazer_login(driver, pin_instalação, senha_instalação):
    url = "https://app6.bempratico.com.br//?p=1&s=login"
    driver.get(url)

    def esperar_elemento_visivel(by, value, timeout=10):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    esperar_elemento_visivel(By.ID, 'v')
    caixa_de_texto = driver.find_element(By.ID, 'v')
    email_login = os.getenv("EMAIL_LOGIN")
    caixa_de_texto.send_keys(email_login)

    esperar_elemento_visivel(By.NAME, "senha")
    campo_senha = driver.find_element(By.NAME, "senha")
    campo_senha.send_keys(senha_instalação)

    esperar_elemento_visivel(By.NAME, "logar")
    botao_entrar = driver.find_element(By.NAME, "logar")
    botao_entrar.click()

    esperar_elemento_visivel(By.ID, "input_desktop")
    campo_pin = driver.find_element(By.ID, "input_desktop")
    campo_pin.send_keys(pin_instalação)

    print(f"Título da página: {driver.title}")