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



# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

def extract_code_from_subject(subject):
    code_pattern = re.compile(r'\b\d{6}\b')  # Pattern to match a 6-digit code
    match = code_pattern.search(subject)
    if match:
        return match.group(0)
    return None

# Function to get the confirmation code from the email
def get_confirmation_code(email_id, app_password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        time.sleep(3)

        # Search for all emails in the inbox
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        time.sleep(2)

        # Fetch the latest email
        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        time.sleep(2)
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        # Extract the subject line
        subject = msg['subject']
        print(f"Email Subject: {subject}")

        # Extract the confirmation code from the subject line
        code = extract_code_from_subject(subject)
        if code:
            print("Confirmation code found in the subject line.")
            return code
        else:
            print("Confirmation code not found in the subject line.")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def mix_automation(email_id,email_password,site_url):
    
    try:
        driver.get(site_url)
        time.sleep(10)

        join_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[1]/div[3]/div/div/div/div/div[1]/button')
        join_btn.click()
        time.sleep(5)

        google_btn=driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r3:"]/div/div/div[2]/form[3]/button')
        google_btn.click()
        time.sleep(5)

        account_btn=driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[2]/div/div/div[2]')
        account_btn.click()
        time.sleep(5)


        # Switch to Google Sign-In iframe
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe[src*="accounts.google.com"]'))
        time.sleep(4)
        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "identifierId"))
        )
        email_field.send_keys(email_id)
        time.sleep(5)
        
        # Click "Next" button
        next_btn = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
        next_btn.click()
        time.sleep(5)

        # Enter password
        password=''
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        )
        password_field.send_keys(password)
        time.sleep(5)

        # Click "Next" button to sign in
        next_btn = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
        next_btn.click()
        time.sleep(8)

        try_another_way=driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div[2]/div[2]/div/div/button')
        try_another_way.click()
        time.sleep(8)

        # Switch back to the main content
        driver.switch_to.default_content()

    except Exception as e:
        print("An error occurred:", str(e))


        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url = 'https://mix.com/'

    response = mix_automation(email_id, email_password,  site_url)
    print(response)