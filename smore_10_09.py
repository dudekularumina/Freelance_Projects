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
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless





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

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument(f"user-agent={USER_AGENT}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

try:
    driver.get('https://www.smore.com/')
    time.sleep(10)

    signup_free=driver.find_element(By.XPATH,'//*[@id="hero-section"]/div/div/div/div[1]/div[3]/a')
    signup_free.click()
    time.sleep(10)

    first_name=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[1]/label/div/input')
    first_name.send_keys('Gaurav')
    time.sleep(15)
    

    last_name=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[2]/label/div/input')
    last_name.send_keys('Thakur')
    time.sleep(15)

    email_input=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/label/div/input')
    email_input.send_keys(EMAIL)
    time.sleep(15)

    password='Gaurav@4122'
    password_input=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[3]/div[3]/div/label/div/input')
    password_input.send_keys(password)
    time.sleep(20)

      
    # Handle reCAPTCHA
    try:
        wait = WebDriverWait(driver, 10)

        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
        driver.switch_to.frame(iframe)
        print("Switched to reCAPTCHA iframe")
        time.sleep(2)

        recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        recaptcha_checkbox.click()
        print("reCAPTCHA checkbox clicked")
        time.sleep(2)

        driver.switch_to.default_content()
        print("Switched back to default content")
        time.sleep(3)

        # Solve reCAPTCHA
        try:
            time.sleep(5)

            site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            current_url = driver.current_url
            captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

            if captcha_solution:
                driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                print("reCAPTCHA response submitted")
        except:
            print("Failed to solve image reCAPTCHA")
            

    except Exception as e:
        print(f"CAPTCHA handling failed: {e}")

    
    create_acc=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[3]/input')
    create_acc.click()
    time.sleep(10)

    check_box=driver.find_element(By.XPATH,'//*[@id="terms"]')
    check_box.click()
    time.sleep(10)

    continue_btn=driver.find_element(By.XPATH,'//*[@id="svelte-d71734b3c738"]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div/input')
    continue_btn.click()
    time.sleep(10)








finally:
    time.sleep(10)
    driver.quit()