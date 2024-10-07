from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import imaplib
import email
from email.header import decode_header
import re
from bs4 import BeautifulSoup


# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
# solver = hCaptchaProxyless()
# solver.set_key(API_KEY)

EMAIL = "gauravthakur81711296@gmail.com"    #gauravthakur81711296
PASSWORD = "ceaj vinr bkvv tpux"
IMAP_SERVER = "imap.gmail.com" 
EMAIL_FOLDER = "inbox"  # or the folder where the confirmation email is located

# Function to fetch the confirmation link from the email
def get_confirmation_link():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select(EMAIL_FOLDER)

    # Search for the email with the subject containing "Confirm your email to get started on Patreon"
    status, data = mail.search(None, 'SUBJECT "Confirm your email to get started on Patreon"')
    if status != 'OK':
        print("Failed to retrieve email.")
        return None

    # Get the list of email IDs
    email_ids = data[0].split()
    if not email_ids:
        print("No emails found.")
        return None

    # Fetch the latest email
    latest_email_id = email_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
    if status != 'OK':
        print("Failed to fetch email.")
        return None

    # Parse the email content
    msg = email.message_from_bytes(msg_data[0][1])
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                html_content = part.get_payload(decode=True).decode()
                break
    else:
        html_content = msg.get_payload(decode=True).decode()

    # Use BeautifulSoup to parse the HTML and extract the link
    soup = BeautifulSoup(html_content, "html.parser")
    confirm_button = soup.find("a", string="Confirm Email")
    if confirm_button and 'href' in confirm_button.attrs:
        return confirm_button['href']
    return None



# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument(f"user-agent={USER_AGENT}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

try:
    driver.get('https://www.ticketleap.com/')
    time.sleep(10)

    start_free=driver.find_element(By.XPATH,'//*[@id="main-header"]/div/div/div/ul/li[2]/a')
    start_free.click()
    time.sleep(20)

    
    email_input=driver.find_element(By.NAME,'attributes.email')
    email_input.send_keys(EMAIL)
    time.sleep(15)

    
    first_name=driver.find_element(By.NAME,'attributes.first_name')
    first_name.send_keys('Gaurav')
    time.sleep(15)
    

    last_name=driver.find_element(By.NAME,'attributes.last_name')
    last_name.send_keys('Thakur')
    time.sleep(15)


    password='Gaurav@4122'
    password_input=driver.find_element(By.NAME,'attributes.password')
    password_input.send_keys(password)
    time.sleep(10)

    org_input=driver.find_element(By.NAME,'attributes.name')
    org_input.send_keys("comde")
    time.sleep(20)

    # org_link_input=driver.find_element(By.NAME,'attributes.slug')
    # org_link_input.send_keys(password)
    # time.sleep(10)

    continue_btn=driver.find_element(By.XPATH,'//*[@id="root"]/main/form/div/div/div[2]/div[7]/button')
    continue_btn.click()
    time.sleep(10)





finally:
    time.sleep(10)
    driver.quit()