import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import zipfile
import os
import tempfile
import shutil
import platform
import urllib.request


class Trubbish(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trubbish - Tweet Deleter")
        self.setFixedSize(300, 200)  # Define o tamanho fixo da janela
    
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#678171"))  # Define o fundo de cor
        self.setPalette(palette)

        # Tamanho da fonte
        font = QFont()
        font.setPointSize(13)
        self.setFont(font)

        # Define o ícone do programa
        icon = QIcon("trubbish.png")
        self.setWindowIcon(icon)

        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.start_button = QPushButton("Start")
        self.deleted_count_label = QLabel("Deleted Count: 0")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.deleted_count_label)

        self.setLayout(layout)

        # Connect signals
        self.start_button.clicked.connect(self.start_deletion)

    def update_deleted_count_label(self, count):
        self.deleted_count_label.setText(f"Deleted Count: {count}")

    def start_deletion(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            self.start_button.setEnabled(False)
            self.delete_tweets(username, password)
            self.start_button.setEnabled(True)

    def get_chromedriver_version(self):
        return '114.0.5735.90'  # Substitua pela versão mais recente do chromedriver disponível

    def download_chromedriver(self):
        desired_location = 'driver'
        
        # Verificar se o chromedriver já existe no local desejado
        if os.path.isfile(os.path.join(desired_location, 'chromedriver.exe')):
            return desired_location
        
        # Verificar a arquitetura do sistema operacional
        if platform.architecture()[0] == '64bit':
            chromedriver_url = f'https://chromedriver.storage.googleapis.com/{self.get_chromedriver_version()}/chromedriver_win32.zip'
        else:
            chromedriver_url = f'https://chromedriver.storage.googleapis.com/{self.get_chromedriver_version()}/chromedriver_win32.zip'

        # Baixar o chromedriver e extrair o arquivo zip
        with tempfile.TemporaryDirectory() as temp_dir:
            download_path = os.path.join(temp_dir, 'chromedriver.zip')
            urllib.request.urlretrieve(chromedriver_url, download_path)
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Mover o arquivo chromedriver para o local desejado
            final_path = os.path.join(temp_dir, 'chromedriver.exe')
            shutil.move(final_path, desired_location)
        
        return desired_location

    def delete_tweets(self, username, password):
        global wait
        # Baixar e configurar o chromedriver
        chromedriver_path = self.download_chromedriver()

        # Configurar o serviço do chromedriver
        service = webdriver.chrome.service.Service(chromedriver_path)

        # Configurar as opções do Chrome
        options = webdriver.ChromeOptions()

        # Inicializar o driver do Chrome
        driver = webdriver.Chrome(service=service, options=options)

        wait = WebDriverWait(driver, 100)
        
        try:
            # Abrir a página de login
            driver.get("https://twitter.com/login")
            time.sleep(8)

            # Preencher o campo de usuário
            username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#layers > div > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-1867qdf.r-1wbh5a2.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1.r-htvplk.r-1udh08x > div > div > div.css-1dbjc4n.r-kemksi.r-6koalj.r-16y2uox.r-1wbh5a2 > div.css-1dbjc4n.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-1ye8kvj.r-13qz1uu > div > div > div > div.css-1dbjc4n.r-mk0yit.r-1f1sjgu.r-13qz1uu > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-1pn2ns4.r-ttdzmv > div > input")))
            username_field.send_keys(username)
            username_field.send_keys(Keys.RETURN)

            # Aguardar a próxima tela e preencher a senha
            time.sleep(3)
            password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Aguardar o login ser concluído
            time.sleep(8)

            # Acessar a página com os tweets do usuário
            driver.get(f"https://twitter.com/{username}/with_replies")
            time.sleep(8)
            
            # Deletar os tweets
            deleted_count = 0
            tweet_index = 0

            while True:
                # Obter os tweets na página
                tweets = driver.find_elements(By.XPATH, '//article[contains(@data-testid, "tweet")]')

                if len(tweets) == 0 or tweet_index >= len(tweets):
                    break

                tweet = tweets[tweet_index]  # Pegar o tweet atual pelo índice

                # Verificar se o tweet pertence ao nome de usuário
                tweet_username_elements = tweet.find_elements(By.CSS_SELECTOR, 'span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')
                tweet_username = None

                for username_element in tweet_username_elements:
                    if "@" in username_element.get_attribute("textContent"):
                        tweet_username = username_element.get_attribute("textContent")
                        break

                if tweet_username is not None:
                    tweet_username = tweet_username.replace('@', '')

                if tweet_username == username:
                    # Encontrar o botão dos três pontinhos no tweet
                    options_button = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="caret"]')

                    ActionChains(driver).move_to_element(options_button).click().perform()
                    time.sleep(1)

                    # Encontrar a opção de excluir tweet
                    delete_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="menu"]//span[text()="Excluir"]')))
                    ActionChains(driver).move_to_element(delete_button).click().perform()
                    time.sleep(1.5)

                    # Confirmar a exclusão do tweet
                    confirm_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')))
                    ActionChains(driver).move_to_element(confirm_button).click().perform()
                    time.sleep(2)

                    deleted_count += 1
                    self.update_deleted_count_label(deleted_count)
                    print(f"Tweet N°{deleted_count} excluído.")
                else:
                    tweet_index += 1  # Incrementar o contador de índice

                time.sleep(1)

            print(f"Total de tweets excluídos: {deleted_count}")

        finally:
            # Fechar o navegador
            driver.quit()

            print('Todos os tweets foram excluídos.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    deleter = Trubbish()
    deleter.show()
    sys.exit(app.exec_())