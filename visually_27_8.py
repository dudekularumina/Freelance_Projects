from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import ElementClickInterceptedException
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.alert import Alert

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


EMAIL = "gauravthakur81711296@gmail.com"
PASSWORD = "ceaj vinr bkvv tpux"


# EMAIL = "d.rumina4122@gmail.com"
# PASSWORD = "akau ftel sutp yjxl"


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


try:
    driver.get('https://visual.ly/')
    time.sleep(10)

    accept_btn=driver.find_element(By.XPATH,'//*[@id="footer"]/div[2]/div/div[2]/button')
    accept_btn.click()
    time.sleep(4)

    driver.get('https://visual.ly/user/register')
    time.sleep(5)

    firstname=driver.find_element(By.ID,'edit-field-first-name-und-0-value')
    firstname.send_keys('Gaurav')
    time.sleep(4)

    lastname=driver.find_element(By.ID,'edit-field-last-name-und-0-value')
    lastname.send_keys('Thakur')
    time.sleep(4)

    email_input=driver.find_element(By.ID,'edit-mail')
    email_input.send_keys(EMAIL)
    time.sleep(4)

    password_input=driver.find_element(By.ID,'edit-pass')
    password_input.send_keys("Gaurav@4122")
    time.sleep(4)

    agree_checkbox=driver.find_element(By.ID,'edit-gdpr-agreement-und')
    agree_checkbox.click()
    time.sleep(4)

    signup_btn=driver.find_element(By.XPATH,'//*[@id="edit-submit"]')
    signup_btn.click()
    time.sleep(5)







finally:
    time.sleep(5)
    driver.quit()