
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

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

EMAIL = "gauravthakur81711296@gmail.com"
PASSWORD = "ceaj vinr bkvv tpux"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


def solve_recaptcha(api_key, site_key, url):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    response = solver.solve_and_return_solution()
    if response != 0:
        print("CAPTCHA Solved: " + response)
        return response
    else:
        print("Failed to solve CAPTCHA: " + solver.error_code)
        return None


try:
   # Open the Pinterest website
    driver.get("https://in.pinterest.com/")
    time.sleep(8)

        # Wait until the button is clickable and click it
    button = driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[1]/div/div[2]/div[3]/button')
    button.click()
    time.sleep(3)

    # Wait for the email input field to be present and enter the email
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("gauravthakur81711296@gmail.com")
    time.sleep(3)


    # Enter the password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("Gaurav@81711296")
    time.sleep(3)


    # Enter the date of birth
    dob_field = driver.find_element(By.ID, "birthdate")
    dob_field.send_keys("04/05/1999")
    time.sleep(3)


    # Wait for the "Continue" button to be clickable and click it
    continue_button = driver.find_element(By.XPATH, "//button[@aria-label='Continue creating your Pinterest account']")
    continue_button.click()
    time.sleep(8)

    # Print the current URL
    current_url = driver.current_url
    print(f"Current URL--------: {current_url}")
    time.sleep(8)

    profile=driver.find_element(By.XPATH, '//*[@id="HeaderContent"]/div/div/div[2]/div/div/div/div[6]/div[4]/div/div/div/a')
    profile.click()
    time.sleep(5)

    driver.get("https://in.pinterest.com/settings/claim")
    time.sleep(5)

        
finally:
    time.sleep(5)
    driver.quit()