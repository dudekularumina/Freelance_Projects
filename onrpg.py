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
from PIL import Image
import pytesseract
import time
import requests
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO
import pytesseract
import urllib.request
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import pytesseract
import easyocr

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
#"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Set the path to the Tesseract-OCR executable if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

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
def onrpg_automation(email_id,email_password,site_url):


    try:
        # Open the website
        driver.get(site_url)
        time.sleep(5)
        driver.get("https://www.onrpg.com/boards/register.php")
        time.sleep(5)


        # Select the month
        month_select_element = driver.find_element(By.ID, "month")
        month_select = Select(month_select_element)
        month_select.select_by_value("05")  # May
        time.sleep(4)

        # Select the day
        day_select_element = driver.find_element(By.ID, "day")
        day_select = Select(day_select_element)
        day_select.select_by_value("04")  # 4th da
        time.sleep(4)

        # Enter the year
        year_input = driver.find_element(By.ID,"year")
        year_input.send_keys("1999")
        time.sleep(4)


        # Click the proceed button
        proceed_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Proceed…']")
        proceed_button.click()

        # Print the URL after clicking the button
        time.sleep(5)  # Wait for the page to load
        print("Current URL after clicking Proceed button:", driver.current_url)
        time.sleep(10)

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(3)

        user_input=driver.find_element(By.ID, "regusername")
        user_input.send_keys("gauravrajput")
        time.sleep(3)

        password1_input=driver.find_element(By.ID, "password")
        password1_input.send_keys("Gaurav@41228")
        time.sleep(4)

        password2_input=driver.find_element(By.ID, "passwordconfirm")
        password2_input.send_keys("Gaurav@41228")
        time.sleep(4)

        email_input=driver.find_element(By.ID, "email")
        email_input.send_keys(email_id)
        time.sleep(3)

        emailconf_input=driver.find_element(By.ID, "emailconfirm")
        emailconf_input.send_keys(email_id)
        time.sleep(3)

        # Download CAPTCHA image
        captcha_img = driver.find_element(By.ID, "imagereg")
        captcha_url = captcha_img.get_attribute("src")
        print("Captcha Image Source:", captcha_url)
        time.sleep(3)

        
        # Fetch the image
        with urllib.request.urlopen(captcha_url) as response:
            img = Image.open(BytesIO(response.read()))

        # Save the original image for debugging
        img.save("original_captcha.png")

        # Initialize EasyOCR reader with English language
        reader = easyocr.Reader(['en'])

        # Perform OCR
        result = reader.readtext(img)

        # Extract and print text from the result
        captcha_text = ' '.join([text[1] for text in result])
        print("Captcha Text Extracted:", captcha_text)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(3)

        check_box=driver.find_element(By.ID, "cb_rules_agree")
        check_box.click()
        time.sleep(3)

        submit=driver.find_element(By.CLASS_NAME, "button")
        submit.click()
        time.sleep(4)

        print("Current URl", driver.current_url)
        time.sleep(8)


        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url = "https://www.onrpg.com/"

    response = onrpg_automation(email_id, email_password,  site_url)
    print(response)