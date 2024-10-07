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

def issuu_automation(main_email, app_pass, username, password, firstname, lastname, signup_url, profile_url, user_email, site_url, signin_url):
        
    # try:
        # Open the website
        driver.get(site_url)
        time.sleep(8)

        cookies_btn=driver.find_element(By.ID,'CybotCookiebotDialogBodyButtonAccept')
        cookies_btn.click()
        time.sleep(5)

        driver.get(signup_url)
        time.sleep(10)

        first_name=driver.find_element(By.ID,'first-name')
        first_name.send_keys(firstname)
        time.sleep(5)

        last_name=driver.find_element(By.ID,'last-name')
        last_name.send_keys(lastname)
        time.sleep(5)

        email_input=driver.find_element(By.ID,'email')
        email_input.send_keys(user_email)
        time.sleep(5)

        username_input=driver.find_element(By.ID,'username')
        username_input.send_keys(username)
        time.sleep(5)

        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(8)

        check_box=driver.find_element(By.XPATH,'//*[@id="app"]/main/div[1]/div/div[1]/div[2]/div/form/div[2]/div/div[1]/span/label/span/span/input')
        driver.execute_script("arguments[0].scrollIntoView(true);",check_box)   
        check_box.click()
        time.sleep(8)

        try:

            signup_btn=driver.find_element(By.XPATH,'//*[@id="app"]/main/div[1]/div/div[1]/div[2]/div/form/div[4]/div/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView(true);",signup_btn)
            
            signup_btn.click()
            time.sleep(6)

        except Exception as e:
            print(f'exception occured',e)


        
        # Handle reCAPTCHA
        try:
            wait = WebDriverWait(driver, 10)

            time.sleep(10)
            iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
            driver.switch_to.frame(iframe)
            print("Switched to reCAPTCHA iframe")
            time.sleep(5)

            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
            recaptcha_checkbox.click()
            print("reCAPTCHA checkbox clicked")
            time.sleep(2)

            driver.switch_to.default_content()
            print("Switched back to default content")
            time.sleep(3)

            # Solve reCAPTCHA
            try:
                time.sleep(15)

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


        time.sleep(10)

        signup_btn=driver.find_element(By.XPATH,'//*[@id="app"]/main/div[1]/div/div[1]/div[2]/div/form/div[4]/div/div/div/button')
        signup_btn.click()
        time.sleep(10)



        # Retrieve the confirmation code from the email
        confirmation_code = get_confirmation_code(main_email, app_pass)

        # Enter the confirmation code in the form
        if confirmation_code:
            verify_code = driver.find_element(By.ID, 'verify-code')
            verify_code.send_keys(confirmation_code)
            time.sleep(5)
        else:
            print("Failed to retrieve the confirmation code.")


        validate_btn=driver.find_element(By.XPATH,'//*[@id="app"]/main/div[1]/div/div[1]/div[2]/div/div/div/form/div[2]/button')
        validate_btn.click()
        time.sleep(10)

        close_btn=driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/button')
        close_btn.click()
        time.sleep(5)

        #===================Login Page===============

        driver.get(signin_url)
        time.sleep(4)

        email_input=driver.find_element(By.ID,'email')
        email_input.send_keys(user_email)
        time.sleep(5)

        
        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(8)

        sigin_btn=driver.find_element(By.XPATH,'//*[@id="app"]/main/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[3]/button')
        sigin_btn.click()
        time.sleep(5)

        
        close_btn=driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/button')
        close_btn.click()
        time.sleep(10)


        # ====================================================================


        time.sleep(10)
        driver.get('https://issuu.com/home/settings')
        time.sleep(10)

        website=driver.find_element(By.ID,'website_textinput')
        driver.execute_script("arguments[0].scrollIntoView(true);",website)
        website.send_keys('https://bluemax11.com')
        time.sleep(8)

        savechanges_btn=driver.find_element(By.XPATH,'//*[@id="app"]/div/div[3]/div[2]/button')
        driver.execute_script("arguments[0].scrollIntoView(true);",savechanges_btn)
        savechanges_btn.click()
        time.sleep(10)

        driver.get(profile_url)#updated
        time.sleep(10)


           
        driver.quit()
        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    # except Exception as e:
    #     print(e)
    #     return f"Error: {e}"

if __name__ == "__main__":
    trial_users = [{"user_email":"user902@additivedecor.com", "username":"gauravraj89","password":"Gaurav@321123"}, {"user_email":"user56@additivedecor.com", "username":"user56789","password":"Gaurav@321123"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]


    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        password = trail_creds["password"]
        firstname='Gaurav'
        lastname='Thakur'


        signup_url='https://issuu.com/signup'
        signin_url='https://issuu.com/signin'
        profile_url=f"https://issuu.com/{username}"
        site_url = "https://issuu.com/"

        response = issuu_automation(main_email, app_pass, username=username, password=password, firstname=firstname, lastname=lastname, signup_url=signup_url, profile_url=profile_url, user_email=user_email, site_url=site_url, signin_url=signin_url)
        print(response)

        time.sleep(10)