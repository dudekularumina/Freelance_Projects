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


# Function to extract the confirmation link from the text
def extract_link_from_text(text):
    url_pattern = re.compile(r'https://www\.magcloud\.com/confirm/[a-z0-9-]+')
    match = url_pattern.search(text)
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

        # Check the subject to see if it contains "MagCloud "
        subject = msg['subject']
        if "MagCloud " in subject:
            print(f"Email Subject: {subject}")

            # Extract all text content from the email
            email_content = extract_text_from_part(msg)

            #============================ Print all the text from the email==============================
            # print("Full Email Content:")
            # print(email_content)

            # Now try to extract the confirmation link using regex
            link = extract_link_from_text(email_content)
            if link:
                print("Confirmation link found in the email.")
                return link
            else:
                print("Confirmation link not found in the email content.")
        else:
            print(f"No MagCloud -related email found. Email Subject: {subject}")

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



def magcloud_automation(main_email, app_pass,password ,username,firstname,lastname,signup_url,login_url,account_url,user_email, site_url):

    try:
        # Open the website
        driver.get(site_url)
        time.sleep(10)
        driver.get(signup_url) #updated
        time.sleep(8)
        
    
        # Fill in the registration details
        first_name = driver.find_element(By.ID, "FirstName")
        first_name.send_keys(firstname)
        time.sleep(3)

        last_name = driver.find_element(By.ID, "LastName")
        last_name.send_keys(lastname)
        time.sleep(3)
        
        
        username_input= driver.find_element(By.ID, "NewUsername")
        username_input.send_keys(username)
        time.sleep(3)
        
        password1 = driver.find_element(By.ID, "Password1")
        password1.send_keys(password)
        time.sleep(3)

        #Confirm  Input password
        password2 = driver.find_element(By.ID, "Password2")
        password2.send_keys(password)
        time.sleep(5)

            # Scroll down by a specific number of pixels (e.g., 500 pixels)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    
        email_input = driver.find_element(By.ID, "PasswordQuestion")
        email_input.send_keys(user_email)
        time.sleep(15)

        
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

        
        signup_button = driver.find_element(By.CSS_SELECTOR, "#sign-up > div:nth-child(1) > div.main > form > p.form-item > button")

        time.sleep(10)
        # Attempt to click using WebDriver first
        try:
            signup_button.click()
        except ElementClickInterceptedException:
            print("Click intercepted, attempting to click using JavaScript...")
            driver.execute_script("arguments[0].click();", signup_button)

        print("Account Created..............")

        print("Current Url After Sign In----------", driver.current_url)
        time.sleep(30) #wait to get the confirmation mail
       
        # Try to get the confirmation link from the email
        confirmation_link = get_confirmation_link(main_email, app_pass)
        time.sleep(5)
        
        if confirmation_link:
            # Print the confirmation link
            print(f"Confirmation Link: {confirmation_link}")

            # Open the confirmation link in the browser
            driver.get(confirmation_link)
            time.sleep(5)  # Wait for the activation page to load


        # #=====================Login Page===========================
        try:
            driver.get(login_url) #updated

            time.sleep(5)

            username_input1=driver.find_element(By.ID, "username")
            username_input1.send_keys(username)
            time.sleep(5)

            password_input1=driver.find_element(By.ID, "password")
            password_input1.send_keys(password)
            time.sleep(5)

            submit=driver.find_element(By.XPATH, '//*[@id="sign-up"]/div[2]/div[2]/form/p[2]/button')
            submit.click()
            time.sleep(3)
            print("Current URL after login,, :", driver.current_url)
        except:
            print("Except Executed.....................")


        #==================================================================

        time.sleep(5)
        accept_button=driver.find_element(By.NAME, "confirm")
        time.sleep(2)
        accept_button.click()
        time.sleep(5)
        print("Current URL after accept.......", driver.current_url)

                
        #=================== Edit Settings On  Profile===================
        driver.get(account_url)#updated
        time.sleep(10)

        
        # Click on the second "Edit" button
        edit_buttons = driver.find_elements(By.CSS_SELECTOR, "a.info-edit-button")
        if len(edit_buttons) > 1:
            driver.execute_script("arguments[0].click();", edit_buttons[1])
            time.sleep(5)
        else:
            print("Second edit button not found")


        # Input the website URL
        website_input = driver.find_element(By.ID, "WebsiteUrl")
        website_input.clear()  # Clear any existing content
        website_input.send_keys("https://www.sample.com")     #Add the sample URl
        time.sleep(3)

        # Input text into the textarea
        profile_textarea = driver.find_element(By.ID, "PublicProfile")
        profile_textarea.clear()  # Clear any existing content
        profile_textarea.send_keys("This is a sample public profile text area.........")
        time.sleep(3)

        # Scroll to the "Save Changes" button
        save_button = driver.find_element(By.CSS_SELECTOR, "a.info-save-button.mc-button.test_submitProfileInfo")
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        time.sleep(3)

        # Click the "Save Changes" button
        driver.execute_script("arguments[0].click();", save_button)
        time.sleep(5)

        # Print the current URL after saving changes
        print("Current URL after saving changes: ", driver.current_url)
        time.sleep(10)

            

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)

if __name__ == "__main__":
    trial_users = [{"user_email":"user9876@additivedecor.com", "username":"gaurav45987","password":"Gaurav@37559"}, {"user_email":"user5467@additivedecor.com", "username":"Thakur564747434","password":"Gaurav@367575623"}]    
    
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

        site_url ="https://www.magcloud.com/"
        signup_url="https://www.magcloud.com/signup"
        login_url="https://www.magcloud.com/login"
        account_url="https://www.magcloud.com/account"

        driver = create_driver()


        response = magcloud_automation(main_email, app_pass,password=password ,username=username,firstname=firstname,lastname=lastname,signup_url=signup_url,login_url=login_url,account_url=account_url,user_email=user_email, site_url=site_url)
        print(response)







