from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import imaplib
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
import re

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()

chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

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
        print("task finished with error " + solver.error_code)
        return None


def extract_link_from_text(text):
    # Regular expression to find URLs in the text
    url_pattern = re.compile(r'(https?://[^\s]+)')
    urls = url_pattern.findall(text)
    for url in urls:
        if "wordpress.org" in url:
            return url
    return None

def get_confirmation_link(email_id, app_password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        time.sleep(3)

        # Search for the most recent email (can use 'UNSEEN' to get unread mails)
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()

        if not email_ids:
            print("No emails found.")
            return None

        # Fetch the most recent email
        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        time.sleep(2)
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        # Initialize email content
        email_content = None

        # Check if the email is multipart
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    email_content = soup.get_text()
                    print("HTML part found. Content:")
                    print(email_content)  # Log the HTML content
                    # Check for "WordPress" in the HTML content
                    if "WordPress" in email_content:
                        link = soup.find('a', href=True)
                        if link:
                            print("Confirmation link found in HTML part.")
                            return link['href']
                elif part.get_content_type() == 'text/plain':
                    email_content = part.get_payload(decode=True).decode()
                    print("Plain text part found. Content:")
                    print(email_content)  # Log the plain text content
                    # Check for "WordPress" in the plain text content
                    if "WordPress" in email_content:
                        link = extract_link_from_text(email_content)
                        if link:
                            print("Confirmation link found in plain text part.")
                            return link
        else:
            if msg.get_content_type() == 'text/html':
                html_content = msg.get_payload(decode=True)
                soup = BeautifulSoup(html_content, 'html.parser')
                email_content = soup.get_text()
                print("HTML email found. Content:")
                print(email_content)  # Log the HTML content
                # Check for "WordPress" in the HTML content
                if "WordPress" in email_content:
                    link = soup.find('a', href=True)
                    if link:
                        print("Confirmation link found in HTML email.")
                        return link['href']
            elif msg.get_content_type() == 'text/plain':
                email_content = msg.get_payload(decode=True).decode()
                print("Plain text email found. Content:")
                print(email_content)  # Log the plain text content
                # Check for "WordPress" in the plain text content
                if "WordPress" in email_content:
                    link = extract_link_from_text(email_content)
                    if link:
                        print("Confirmation link found in plain text email.")
                        return link

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        imap.logout()

def element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except:
        return False
def bbpress_automation(main_email, app_pass,password ,username,login_url,user_email, site_url):
    try:
        #==========================Register Page =============
        driver.get(site_url)

        username_input = driver.find_element(By.ID, "user_login")
        time.sleep(2)
        username_input.send_keys(username)
        time.sleep(10)

        email_input = driver.find_element(By.ID, "user_email")
        time.sleep(2)
        email_input.send_keys(user_email)
        time.sleep(5)

        terms_checkbox = driver.find_element(By.ID, "terms_of_service")
        if not terms_checkbox.is_selected():
            terms_checkbox.click()
        time.sleep(5)

        mailing_list_checkbox = driver.find_element(By.ID, "user_mailinglist")
        if not mailing_list_checkbox.is_selected():
            mailing_list_checkbox.click()
        time.sleep(5)

        if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
            site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            current_url = driver.current_url
            recaptcha_response = solve_recaptcha(site_key, current_url)

            if recaptcha_response:
                driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
                time.sleep(2)
                create_account_button = driver.find_element(By.ID, "wp-submit")
                time.sleep(3)
                create_account_button.click()
        else:
            create_account_button = driver.find_element(By.ID, "wp-submit")
            time.sleep(3)
            driver.execute_script("arguments[0].scrollIntoView(true);",create_account_button)
            create_account_button.click()

        time.sleep(10)

        

        confirmation_link = get_confirmation_link(main_email, app_pass)
        if confirmation_link:
            driver.get(confirmation_link)
            time.sleep(2)
            #===================After getting Confirmation mail account Creation=================
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass1")))
           
            password_input = driver.find_element(By.ID, "pass1")
            time.sleep(2)
            password_input.clear()
            time.sleep(2)
            password_input.send_keys(password)

            website_input = driver.find_element(By.ID, "user_url")
            time.sleep(2)
            website_input.send_keys("https://mysiteus.com")

            location_input = driver.find_element(By.ID, "user_location")
            time.sleep(2)
            location_input.send_keys("Bangalore")

            occupation_input = driver.find_element(By.ID, "user_occupation")
            time.sleep(2)
            occupation_input.send_keys("Developer")

            interests_input = driver.find_element(By.ID, "user_interests")
            time.sleep(2)
            interests_input.send_keys("technology, innovation")

            if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
                site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                current_url = driver.current_url
                recaptcha_response = solve_recaptcha(site_key, current_url)

                if recaptcha_response:
                    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
                    time.sleep(2)
                
                    create_account_button = driver.find_element(By.ID, "wp-submit")
                    time.sleep(2)
                    if create_account_button:
                        create_account_button.click()
                        time.sleep(10)
                    else:
                        save_profile=driver.find_element(By.CLASS_NAME, "g-recaptcha")
                        save_profile.click()
                        time.sleep(5)
        

                    time.sleep(10)

                    url=driver.current_url
                    print("Current URL----- ", url)
                    time.sleep(10)

                    #=======================Login Page============================
                                    

                    driver.get(login_url) #Updated
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

                    # Click on the specified href link
                    link = driver.find_element(By.XPATH, "//a[@href='https://login.wordpress.org/?from=bbpress.org&redirect_to=https%3A%2F%2Fbbpress.org%2Fabout%2Fintegration%2F&locale=en_US']")
                    link.click()
                    time.sleep(10)

                    username_input1 = driver.find_element(By.ID, "user_login")
                    time.sleep(2)
                    username_input1.send_keys(username)   #

                    password_input = driver.find_element(By.ID, "user_pass")
                    time.sleep(2)
                    password_input.send_keys(password)

                    if element_exists(driver, By.CLASS_NAME, 'g-recaptcha'):
                        site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                        current_url = driver.current_url
                        recaptcha_response = solve_recaptcha(site_key, current_url)
                    try:
                        if recaptcha_response:
                            driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
                            time.sleep(2)
                            login_button = driver.find_element(By.ID, "wp-submit")
                            time.sleep(2)
                            login_button.click()
                    except:
                        login_button = driver.find_element(By.ID, "wp-submit")
                        time.sleep(2)
                        login_button.click()
                    
                    # Navigate to the edit profile page
                    edit_url = f"https://bbpress.org/forums/profile/{username}/edit/"
                    driver.get(edit_url)
                    time.sleep(10)

                    # Clear and update the URL input field
                    url_input = driver.find_element(By.ID, "url")
                    time.sleep(3)
                    url_input.clear()  # Clear the existing text
                    time.sleep(3)
                    url_input.send_keys("https://www.modafinillab.com")  # Enter new URL

                    # Click the update profile button
                    time.sleep(3)
                    update_button = driver.find_element(By.ID, "bbp_user_edit_submit")
                    update_button.click()

                    # Optionally, wait for some confirmation or completion
                    time.sleep(15)
                    print("Current URL---------------",driver.current_url)
                    time.sleep(10)    

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    trial_users = [{"user_email":"user902@additivedecor.com", "username":"gauravraj78654","password":"Gaurav@32176873"}, {"user_email":"user56@additivedecor.com", "username":"user765789","password":"Gaurav@32765723"}]    
    
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

       
        login_url="https://bbpress.org/about/integration/"    #updated
        site_url = "https://login.wordpress.org/register?locale=en_US"

        response = bbpress_automation(main_email, app_pass, username=username, password=password,login_url=login_url,user_email=user_email, site_url=site_url )
        print(response)



