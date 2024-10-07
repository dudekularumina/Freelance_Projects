#==========Working Fine upto Choose the "Open A Chest " Step=============== 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re

def extract_link_from_text(text):
    urls = re.findall(r'(https?://[^\s)]+)', text)  # Improved regex to avoid trailing ')'
    return urls[0] if urls else None

def get_confirmation_link(email_id, app_password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        time.sleep(3)

        # Search for all emails in the inbox
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()

        # Get the latest email ID
        latest_email_id = email_ids[-1]

        # Fetch the latest email
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        time.sleep(2)
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        # Initialize email content
        email_content = ""

        # Check if the email is multipart
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    email_content += soup.get_text()
                elif part.get_content_type() == 'text/plain':
                    email_content += part.get_payload(decode=True).decode()
        else:
            if msg.get_content_type() == 'text/html':
                html_content = msg.get_payload(decode=True)
                soup = BeautifulSoup(html_content, 'html.parser')
                email_content = soup.get_text()
            elif msg.get_content_type() == 'text/plain':
                email_content = msg.get_payload(decode=True).decode()

        # Print the content of the latest email
        print("Latest Email Content:")
        print(email_content)

        # Extract confirmation link if it's from the relevant sender (e.g., Armor Games)
        if "Armor Games" in email_content:
            link = extract_link_from_text(email_content)
            if link:
                print("Confirmation link found in email content.")
                return link

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        imap.logout()

    return None


# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def solve_recaptcha(site_key, url):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(url)
    solver.set_website_key(site_key)

    response = solver.solve_and_return_solution()
    if response != 0:
        return response
    else:
        print("Task finished with error: " + solver.error_code)
        return None
def armorgames_automation(main_email, app_pass,password ,username,register_url,quests_url,user_email, display_name,  about_content, site_url):
    try:
        # Open Armor Games registration page
        driver.get(site_url)

        register = driver.find_element(By.CLASS_NAME, "create-account")
        register.click()
        time.sleep(5)
        driver.get(register_url)     #updated
        
        username_input= driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(5)

        email_input= driver.find_element(By.ID, "email")
        email_input.send_keys(main_email)
        time.sleep(5)

        password_input= driver.find_element(By.ID, "password")
        password_input.send_keys(password)     #Gaurav@81711296
        time.sleep(5)

        checkbox = driver.find_element(By.ID, "agree-tos")
        checkbox.click()
        time.sleep(5)

        register_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-block.btn-warning.btn-armorgames")
        time.sleep(3)
        register_button.click()
        time.sleep(5)

        print("Registration button clicked.")

        time.sleep(10)  # Give time for the page to load the reCAPTCHA
        try:
            site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
            url = driver.current_url
            recaptcha_response = solve_recaptcha(site_key, url)

            if recaptcha_response:
                driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(recaptcha_response))
                time.sleep(3)
                submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-action')]")
                submit_button.click()
                time.sleep(10)
            else:
                print("Failed to solve reCAPTCHA")
        except:
            print("No reCAPTCHA found.")

    
        time.sleep(20)

    
    
        confirmation_link = get_confirmation_link(main_email, app_pass)
        time.sleep(10)
        try:
            if confirmation_link:
                print("Confirmation link:", confirmation_link)

                driver.get(confirmation_link)
                print("Confirmation link opened.")
                time.sleep(10)
                
                # Click the activation button
                activate_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-block.btn-warning.btn-armorgames.text-center")
                activate_button.click()
                print("Activation button clicked.")
                
                # Wait for 20 seconds to observe the result
                time.sleep(20)
                    
        except:
            print("Confirmation link not found.")

        print("Current URL========", driver.current_url)
        driver.get(driver.current_url)
        time.sleep(5)

        driver.get(quests_url)   #updated
        time.sleep(5)
        easy_check=driver.find_element(By.ID, "easy")
        easy_check.click()
        time.sleep(3)

    

        return  {"status": "success", "message": "CLicked easy btn play games to Complete the Quest..", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    trial_emails = ["user4@additivedecor.com", "user5@additivedecor.com", "user6@additivedecor.com", "user7@additivedecor.com"]
    for trail_mail in trial_emails:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_mail
        display_name = 'gaurav'
    
    about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    username='gauravthakur658'
    password='Gaurav@4122'
    register_url="https://armorgames.com/register/email"
    quests_url="https://armorgames.com/quests"
    site_url = "https://armorgames.com/"

    response = armorgames_automation(main_email, app_pass,password ,username,register_url,quests_url,user_email, display_name,  about_content, site_url)
    print(response)
    time.sleep(10)
        

