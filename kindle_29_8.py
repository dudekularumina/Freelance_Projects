from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.webdriver.common.keys import Keys
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

#email_id = "gauravthakur81711296@gmail.com"
#app_password = "ceaj vinr bkvv tpux"
# Email account credentials

EMAIL = "d.rumina4122@gmail.com"
PASSWORD = "akau ftel sutp yjxl"

# EMAIL = "gauravthakur81711296@gmail.com"
# PASSWORD = "ceaj vinr bkvv tpux"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


# Function to extract the confirmation code from the email text
def extract_code_from_text(text):
    code_pattern = re.compile(r'\b[A-Z0-9]{8}\b')
    match = code_pattern.search(text)
    if match:
        return match.group(0)
    return None

# Recursive function to extract text from email parts
def extract_text_from_part(part):
    text_content = ""
    if part.is_multipart():
        for subpart in part.iter_parts():
            text_content += extract_text_from_part(subpart)
    else:
        content_type = part.get_content_type()
        if content_type == 'text/plain':
            text_content += part.get_payload(decode=True).decode()
        elif content_type == 'text/html':
            html_part = part.get_payload(decode=True).decode()
            soup = BeautifulSoup(html_part, 'html.parser')
            text_content += soup.get_text()
    return text_content

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

        # Check the subject to see if it contains "Issuu"
        subject = msg['subject']
        if "Issuu" in subject:
            print(f"Email Subject: {subject}")

            # Extract all text content from the email
            email_content = extract_text_from_part(msg)

            # Extract the confirmation code using regex
            code = extract_code_from_text(email_content)
            if code:
                print("Confirmation code found in the email.")
                return code
            else:
                print("Confirmation code not found in the email content.")
        else:
            print(f"No Issuu-related email found. Email Subject: {subject}")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
    # Open the website
    driver.get("https://www.amazon.com/")
    time.sleep(8)

    driver.get("https://www.amazon.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgift-cards%2Fb%2F%3F_encoding%3DUTF8%26ie%3DUTF8%26node%3D2238192011%26ref_%3Dnav_newcust&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    time.sleep(8)
    
    user_name=driver.find_element(By.ID,'ap_customer_name')
    user_name.send_keys('Rumi D')
    time.sleep(5)

    email_input=driver.find_element(By.ID,'ap_email')
    email_input.send_keys(EMAIL)
    time.sleep(5)
    
    password='Dudekula@4122'
    password_input=driver.find_element(By.ID,'ap_password')
    password_input.send_keys(password)
    time.sleep(5)

    confm_password_input=driver.find_element(By.ID,'ap_password_check')
    confm_password_input.send_keys(password)
    time.sleep(5)

    continue_btn=driver.find_element(By.XPATH,'//*[@id="continue"]')
    continue_btn.click()
    time.sleep(30)




finally:
    time.sleep(5)
    driver.quit()