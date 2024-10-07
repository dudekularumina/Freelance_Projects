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


# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'
 

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Function to extract the confirmation code from the Quora email text
def extract_code_from_text(text):
    code_pattern = re.compile(r'Your confirmation code is:\s*(\d{6})')
    match = code_pattern.search(text)
    if match:
        return match.group(1)
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
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        time.sleep(3)

        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        time.sleep(2)

        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        time.sleep(2)
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        subject = msg['subject']
        if "Confirmation" in subject:
            email_content = extract_text_from_part(msg)
            code = extract_code_from_text(email_content)
            if code:
                return code
            else:
                print("Confirmation code not found in the email content.")
        else:
            print(f"No Quora -related email found. Email Subject: {subject}")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# # Locate the iframe containing the reCAPTCHA
# iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")

# # Extract the sitekey from the iframe's src attribute
# sitekey_url = iframe.get_attribute("src")
# site_key = sitekey_url.split("k=")[1].split("&")[0]

# print(f"Site Key Found: {site_key}")
    
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
def quora_automation(main_email, app_pass,password ,username,firstname,lastname,user_email, display_name,  about_content, site_url):

    try:
        driver.get(site_url)
        time.sleep(5)

        # Step 1: Click the "Sign up with email" button
        signup=driver.find_elokement(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/button")
        signup.click()
        time.sleep(5)

        # Step 2: Fill out the registration form
        profile_name=driver.find_element(By.ID, "profile-name")
        profile_name.send_keys(username)
        time.sleep(5)

        email= driver.find_element(By.ID, "email")
        email.send_keys(main_email)
        time.sleep(5)

        next_btn= driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/button')
        next_btn.click()
        # time.sleep(5)


        # Wait for email confirmation
        time.sleep(20)  # Adjust sleep as necessary

        # Get confirmation code from email
        confirmation_code = get_confirmation_code(main_email, app_pass)
        if confirmation_code:
            confirm_code=driver.find_element(By.ID, "confirmation-code")
            confirm_code.send_keys(confirmation_code)
            time.sleep(8)

            next_btn1=driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div/button')
            next_btn1.click()
            time.sleep(5)

            # Step 4: Fill out the password field
            password=driver.find_element(By.ID, "password")
            password.send_keys(password)
            time.sleep(5)

                    
            # Handle reCAPTCHA
            try:
                wait = WebDriverWait(driver, 10)
                time.sleep(10)

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
                time.sleep(10)

                # Solve reCAPTCHA
                try:
                    time.sleep(5)
                    # Locate the iframe containing the reCAPTCHA
                    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")

                    # Extract the sitekey from the iframe's src attribute
                    sitekey_url = iframe.get_attribute("src")
                    site_key = sitekey_url.split("k=")[1].split("&")[0]

                    print(f"Site Key Found: {site_key}")

                    # site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                    current_url = driver.current_url
                    captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

                    if captcha_solution:
                        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                        print("reCAPTCHA response submitted")
                except:
                    print("Failed to solve image reCAPTCHA")
                    

            except Exception as e:
                print(f"CAPTCHA handling failed: {e}")
            time.sleep(20)
            
            finish_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div/div/button')
            # driver.execute_script("arguments[0].scrollIntoView();", finish_btn)
            if finish_btn.is_enabled():
                finish_btn.click()
            else:
                print("Button is disabled, cannot click.")
            time.sleep(10)
        #============Login Page================
        # driver.get('https://www.quora.com/')
        # time.sleep(4)
        # email_input=driver.find_element(By.ID,'email')
        # email_input.send_keys('d.rumina4122@gmail.com')
        # time.sleep(4)

        # pwd_input=driver.find_element(By.ID,'password')
        # pwd_input.send_keys('Rumi@4122')
        # time.sleep(4)
        # try:
        #     wait = WebDriverWait(driver, 10)
        #     time.sleep(10)

        #     iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
        #     driver.switch_to.frame(iframe)
        #     print("Switched to reCAPTCHA iframe")
        #     time.sleep(2)

        #     recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        #     recaptcha_checkbox.click()
        #     print("reCAPTCHA checkbox clicked")
        #     time.sleep(2)

        #     driver.switch_to.default_content()
        #     print("Switched back to default content")
        #     time.sleep(10)
        #     try:
        #         time.sleep(5)#recaptcha-response
        #         # Locate the iframe containing the reCAPTCHA
        #         iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")

        #         # Extract the sitekey from the iframe's src attribute
        #         sitekey_url = iframe.get_attribute("src")
        #         site_key = sitekey_url.split("k=")[1].split("&")[0]

        #         print(f"Site Key Found: {site_key}")

        #         # site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha-response').get_attribute('data-sitekey')
        #         current_url = driver.current_url
        #         captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

        #         if captcha_solution:
        #             driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
        #             print("reCAPTCHA response submitted")
        #             time.sleep(10)

        #             # driver.switch_to.default_content()
        #             # print("Switched back to default content")
        #             # time.sleep(10)
        #     except:
        #         print("Failed to solve image reCAPTCHA")


                
        # except Exception as e:
        #     print(f"CAPTCHA handling failed: {e}")
        #     time.sleep(10)

        # login_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[5]/button')
        # login_btn.click()
        # time.sleep(10)

        # profile=driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div[2]')
        # profile.click()
        # time.sleep(3)

        # profile_link=driver.find_element(By.XPATH,'//*[@id="POPOVER28"]/div/div[1]/div/div/div[1]/a')
        # profile_link.click()
        # time.sleep(4)

        # print("Current URL", driver.current_url)

        # desc_link=driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div[2]/div/div')
        # desc_link.click()
        # time.sleep(3)

        # description=driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div')
        # description.send_keys("Here's where the Backlink Appears......")
        # time.sleep(5)
        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


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
    firstname='Gaurav'
    lastname='Thakur'

    site_url = "https://www.quora.com/"

    response = quora_automation(main_email, app_pass,password ,username,firstname,lastname,user_email, display_name,  about_content, site_url)
    print(response)