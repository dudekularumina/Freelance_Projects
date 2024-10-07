from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless



API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


def create_driver():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# Recursive function to extract text and links from email parts
def extract_link_from_part(part):
    if part.is_multipart():
        for subpart in part.iter_parts():
            link = extract_link_from_part(subpart)
            if link:
                return link
    else:
        content_type = part.get_content_type()
        if content_type == 'text/html':
            html_part = part.get_payload(decode=True).decode()
            soup = BeautifulSoup(html_part, 'html.parser')
            # Look for the button or link that says "Verify my email address"
            verify_button = soup.find('a', string="Verify my email address")
            if verify_button and 'href' in verify_button.attrs:
                return verify_button['href']
    return None

# Function to get the confirmation link from the email
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
        time.sleep(2)

        # Fetch the latest email
        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        time.sleep(2)
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        # Check the subject to see if it contains "TED"
        subject = msg['subject']
        if "TED" in subject:
            print(f"Email Subject: {subject}")

            # Extract the link from the email
            confirmation_link = extract_link_from_part(msg)
            if confirmation_link:
                print("Confirmation link found in the email.")
                return confirmation_link
            else:
                print("Confirmation link not found in the email content.")
        else:
            print(f"No TED-related email found. Email Subject: {subject}")

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
def ted_automation(main_email,app_pass,user_email,site_url,signup_url):

    try:
        driver.get(site_url)
        time.sleep(2)

        # Wait for the "Confirm My Choices" button and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "save-preference-btn-handler"))
        ).click()
        print("Cookies consent button clicked.")

        # Open the TED sign-up page
        driver.get(signup_url)
        time.sleep(8)

        # Input the email
        email_field = driver.find_element(By.NAME, "username")
        email_field.send_keys(user_email)
        time.sleep(5)

        # Click on the "Continue" button
        continue_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div/span/span/button')
        continue_button.click()
        time.sleep(8)

        # Input the password
    
        password_field = driver.find_element(By.CLASS_NAME, "css-1knpzs-base")
        password_field.send_keys(password)
        time.sleep(5)

        # Handle reCAPTCHA
        try:
                # Wait for the reCAPTCHA iframe and switch to it
            wait = WebDriverWait(driver, 20)
            iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            driver.switch_to.frame(iframe)
            print("Switched to reCAPTCHA iframe")

            # Click on the reCAPTCHA checkbox
            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
            recaptcha_checkbox.click()
            print("reCAPTCHA checkbox clicked")
            time.sleep(2)

            # Switch back to the main content
            driver.switch_to.default_content()
            print("Switched back to default content")
            time.sleep(5)

            # Attempt to solve reCAPTCHA via API
            site_key = driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']").get_attribute("src").split("k=")[1].split("&")[0]
            current_url = driver.current_url
            captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

            if captcha_solution:
                # Execute script to insert the solved CAPTCHA response
                driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                print("reCAPTCHA response submitted")

            
        except Exception as e:
            print(f"CAPTCHA handling failed: {e}")

        
        time.sleep(8)
        # Click on the "Continue" buttonjjj
        continue_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/span/span/button')
        time.sleep(3)
        continue_button.click()
        time.sleep(8)

        # Input the first name and last name
        first_name_field = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/form/label[1]/input")
        first_name_field.send_keys(firstname)
        time.sleep(5)
    
        last_name_field = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/form/label[2]/input")
        last_name_field.send_keys(lastname)
        time.sleep(5)

        # Click on the final "Continue" button
        final_continue_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/form/p/span/span/button")
        final_continue_button.click()

        time.sleep(5)

        # Fetch and click the confirmation link from the email
        confirmation_link = get_confirmation_link(main_email, app_pass)
        if confirmation_link:
            driver.get(confirmation_link)
            time.sleep(100)
            print("Account verification completed.")
        else:
            print("Confirmation link not found in email.")

        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(20)


if __name__ == "__main__":
    trial_users = [{"user_email":"user8755568@additivedecor.com", "password":"Gaurav@8778778"},
                   {"user_email":"user45668678@additivedecor.com", "password":"Thakur@3638458"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        password = trail_creds["password"]
        firstname='Gaurav'
        lastname='Thakur'
   

        site_url="https://www.ted.com"
        signup_url="https://auth.ted.com/users/new"

        driver=create_driver()

        response = ted_automation(main_email,app_pass,user_email=user_email,  site_url=site_url,signup_url=signup_url)
        print(response)