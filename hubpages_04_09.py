from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.common.exceptions import ElementClickInterceptedException
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import imaplib
import re
from bs4 import BeautifulSoup
from email.policy import default


# Anti-Captcha API key
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
    
# Function to extract the verification link from the email using regular expressions
def extract_verification_link(email_body):
    # Define a regex pattern that matches the verification URL
    pattern = r'https://hubpages\.com/verify/\d+'
    match = re.search(pattern, email_body)
    if match:
        return match.group(0)  # Return the full URL
    return None

# Recursive function to extract HTML or text from email parts
def extract_text_from_part(part):
    if part.is_multipart():
        for subpart in part.iter_parts():
            result = extract_text_from_part(subpart)
            if result:
                return result
    elif part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
        return part.get_payload(decode=True).decode()
    return None

# Function to get the verification link from the latest email
def get_verification_link(email_id, app_password):
    try:
        # Connect to Gmail's IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')

        # Search for all emails in the inbox
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()

        # Fetch the latest email
        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        msg = BytesParser(policy=default).parsebytes(msg_data[0][1])

        # Extract the email body (HTML or plain text)
        email_body = extract_text_from_part(msg)

        if email_body:
            link = extract_verification_link(email_body)
            if link:
                print("Verification link found:", link)
                return link
            else:
                print("Verification link not found in the email.")
        else:
            print("No text content found in the email.")
        
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        imap.logout()


def hubpages_automation(main_email, app_pass,password ,username,new_user_url,user_email,site_url):
        
    try:
        driver.get(site_url)
        time.sleep(10)

        driver.get(new_user_url)
        time.sleep(8)

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(10)

        username_input=driver.find_element(By.ID,'usname3')
        username_input.send_keys(username)
        time.sleep(5)

        email_input=driver.find_element(By.ID,'usemail3')
        email_input.send_keys(user_email)
        time.sleep(5)
        
        
        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(5)

        password_input1=driver.find_element(By.ID,'password2')
        password_input1.send_keys(password)
        time.sleep(8)
        
        # Wait for the checkbox to be clickable
        checkbox=driver.find_element(By.ID, 'eula')
        driver.execute_script("arguments[0].scrollIntoView(true);",checkbox)
        checkbox.click()
        time.sleep(10)

        # Solve CAPTCHA if possible, otherwise proceed to force form submission

        try:
            # Attempt to solve CAPTCHA
            wait = WebDriverWait(driver, 20)

            # Locate the reCAPTCHA iframe and switch to it
            iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
            driver.switch_to.frame(iframe)

            # Click on the reCAPTCHA checkbox
            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
            recaptcha_checkbox.click()

            # Switch back to the main content
            driver.switch_to.default_content()

            # Solve reCAPTCHA if possible
            site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            current_url = driver.current_url
            captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

            if captcha_solution:
                # Insert reCAPTCHA solution
                driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                print("reCAPTCHA response submitted")
            else:
                print("Could not solve CAPTCHA, proceeding without it.")

        except Exception as e:
            print(f"Failed to handle CAPTCHA: {e}")

        # Force enable the Sign Up button and submit the form
        try:
            # Remove any "disabled" attribute from the button
            driver.execute_script("document.getElementById('create_account').removeAttribute('disabled');")

            # Manually trigger the form submission
            driver.execute_script("su.save(false, true);")
            print("Form submission triggered.")
            
            time.sleep(10)

        except Exception as e:
            print(f"Error enabling the button or submitting the form: {e}")
        time.sleep(15)
        print("Account Created..............")
        print("Current Url After Sign In----------", driver.current_url)

        time.sleep(10)

        profile=driver.find_element(By.XPATH,'//*[@id="actions_profile"]/a')
        profile.click()
        time.sleep(10)

        edit_profile=driver.find_element(By.XPATH,'//*[@id="profile_header"]/div[2]/a')
        edit_profile.click()
        time.sleep(10)

        add_website=driver.find_element(By.ID,'website')
        driver.execute_script("arguments[0].scrollIntoView(true);",add_website)
        add_website.send_keys('https://www.sample.com')
        time.sleep(6)

        save_btn=driver.find_element(By.XPATH,'//*[@id="submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);",save_btn)
        save_btn.click()
        time.sleep(5)

        print("Changes Saved..........")

        
        # After completing the registration form, get the confirmation link
        confirmation_link = get_verification_link(main_email, app_pass)
        if confirmation_link:
            # Navigate to the confirmation link
            driver.get(confirmation_link)
            time.sleep(10)
            print("Navigated to the confirmation link successfully.")

        time.sleep(10)

        username_input1=driver.find_element(By.ID,'us1shem2')
        username_input1.send_keys(username)
        time.sleep(5)

        password_input2=driver.find_element(By.ID,'us1sisma2')
        password_input2.send_keys(password)
        time.sleep(5)

        signin_btn=driver.find_element(By.XPATH,'//*[@id="signin_button"]')
        signin_btn.click()
        time.sleep(5)


        publish_article=driver.find_element(By.XPATH,'//*[@id="todolist"]/ol/li[3]/a')
        publish_article.click()
        time,slice(5)

        article_title=driver.find_element(By.NAME,'title')
        article_title.send_keys('My First Article')
        time.sleep(5)

        # Wait until the dropdown is present
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//select[@tabindex="3"]')))

        # Initialize the Select class with the dropdown WebElement
        select = Select(dropdown)
        try:

            select.select_by_visible_text("Arts and Design")
        except:
            select.select_by_value("2") 

        time.sleep(5)

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

        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(10)

        continue_btn=driver.find_element(By.XPATH,'//*[@id="tNT"]/input')
        try:
           continue_btn.click()
           time.sleep(10)
        except ElementClickInterceptedException:
            print("Click intercepted, attempting to click using JavaScript...")
            driver.execute_script("arguments[0].click();", continue_btn)

        article_summary=driver.find_element(By.XPATH,'//*[@id="hubtool_summary"]')
        article_summary.send_keys("What's Art & Design? Any creative human activity can arguably be defined as art. The most well-known art forms are the visual arts, such as painting and sculpture. This subject area also includes design disciplines.")
        time.sleep(5)

        publish_btn=driver.find_element(By.XPATH,'//*[@id="Publish_btn"]')
        publish_btn.click()
        time.sleep(10)

        # Wait for the alert to appear
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # Switch to the alert and print its text
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        time.sleep(5)

        # Accept the alert to close it
        # alert.accept()

        print("Current URL",driver.current_url)
        time.sleep(5)

    

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    trial_users = [{"user_email":"user7655@additivedecor.com", "username":"gaurav56544","password":"Gaurav@3455799"}, {"user_email":"user56117@additivedecor.com", "username":"Thakur5624443","password":"Thakur@352524"}]    
    
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
    
    
    
        site_url = 'https://discover.hubpages.com/'
        new_user_url='https://hubpages.com/user/new/'

        driver = create_driver()


        response = hubpages_automation(main_email, app_pass,password=password ,username=username,new_user_url=new_user_url,user_email=user_email, site_url=site_url)
        print(response)
        time.sleep(10)