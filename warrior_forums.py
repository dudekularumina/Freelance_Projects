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
from selenium.webdriver.common.alert import Alert

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'





# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


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
            # Look for the button or link that says "Activate my account now"
              # Find the element using XPath
            verify_button = soup.select_one('a[href*="warriorforum.com/register.php"]')
            if verify_button:
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

        # Check the subject to see if it contains "Warrior"
        subject = msg['subject']
        if "Warrior" in subject:
            print(f"Email Subject: {subject}")

            # Extract the link from the email
            confirmation_link = extract_link_from_part(msg)
            if confirmation_link:
                print("Confirmation link found in the email.")
                return confirmation_link
            else:
                print("Confirmation link not found in the email content.")
        else:
            print(f"No Warrior-related email found. Email Subject: {subject}")

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

def warriorforums_automation(main_email, app_pass,username,password,user_email,settings_url,profile_url,profile_sec_url, site_url):
    
    try:
        driver.get(site_url)
        time.sleep(5)

        signup=driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[3]/div[2]/div[2]/a')
        signup.click()
        time.sleep(5)

        username_input=driver.find_element(By.ID,'username')
        username_input.send_keys(username)
        time.sleep(5)
    
        email_input=driver.find_element(By.NAME,'email')
        driver.execute_script("arguments[0].scrollIntoView(true);",email_input)
        email_input.send_keys(user_email)
        time.sleep(5)
        
        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)     #Gaurav@4122
        time.sleep(8)

        
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





        signup_btn=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div[2]/form/fieldset/ol/li[5]/button')
        driver.execute_script("arguments[0].scrollIntoView(true);",signup_btn)   
        signup_btn.click()
        time.sleep(5)

        print('CurrentURL===',driver.current_url)
        time.sleep(5)

        join_now=driver.find_element(By.XPATH,'/html/body/main/div[1]/section/div[1]/div/button')
        driver.execute_script("arguments[0].scrollIntoView(true);",join_now)
        join_now.click()
        time.sleep(5)


        time.sleep(10)
        try:
            skip_btn=driver.find_element(By.XPATH,'/html/body/main/div[1]/div/div/button[1]')
            skip_btn.click()
            time.sleep(20)

            close_btn=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/a')
            close_btn.click()
            time.sleep(10)
        except:
            print("No skip and close button---------")

            #=============email membership Confirmation============
        # Fetch and click the confirmation link from the email
        try:
            time.sleep(10) 
            confirmation_link = get_confirmation_link(main_email,app_pass)
            if confirmation_link:
                driver.get(confirmation_link)
                time.sleep(10)
                print("Account verification completed.")
            else:
                print("Confirmation link not found in email.")

            time.sleep(10)
        except Exception as e:
            print("Confirmation link not clicked----")
            print(f"Eception Ocuured",e)


        time.sleep(5)
        try:
            alert = driver.switch_to.alert
            alert.accept()  # Clicks the OK button on the alert
            print("Alert handled successfully.")
        except:
            print("No alert found.")

        #===================   Login Page      ===============
        # try:

        #     driver.get('https://www.warriorforum.com/login/')
        #     time.sleep(5)
        #     username="dudekularumina"

        #     username_input=driver.find_element(By.ID,'username')
        #     username_input.send_keys(username)
        #     time.sleep(5)

        #     pwd_input=driver.find_element(By.ID,'password')
        #     pwd_input.send_keys("Dudekula@4122")
        #     time.sleep(5)

            
        #     # Remove the 'disabled' attribute using JavaScript
        #     login_btn = driver.find_element(By.XPATH, '//button[contains(text(),"Log in")]') 
        #     driver.execute_script("arguments[0].removeAttribute('disabled');", login_btn)

        #     # Wait and click the login button
        #     driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        #     login_btn.click()
        # except Exception as e:
        #     print(f"Exception ",e)
            # driver.quit()
        #====================================================
    
        time.sleep(5)
        
        driver.get(settings_url)
        time.sleep(8)

        driver.get(profile_url)
        time.sleep(10)

        location=driver.find_element(By.ID,'ctb_field2')
        location.clear()
        location.send_keys('India')
        time.sleep(8)
        
        home_page_url=driver.find_element(By.ID,'tb_homepage')
        location.clear()
        driver.execute_script("arguments[0].scrollIntoView(true);",home_page_url)
        home_page_url.send_keys('https://www.samplelink.com/')      #Backlink
        time.sleep(5)

        save_chngs_btn=driver.find_element(By.XPATH,'//*[@id="profileform"]/table[3]/tbody/tr[2]/td/div[2]/input[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);",save_chngs_btn)
        save_chngs_btn.click()
        time.sleep(5)

        print("Current Url====",driver.current_url)
        time.sleep(5)

        driver.get(profile_sec_url)
        time.sleep(10)


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
    site_url = 'https://www.warriorforum.com/'
    settings_url='https://www.warriorforum.com/usercp.php?utm_source=internal&utm_medium=user-menu&utm_campaign=settings'
    profile_url='https://www.warriorforum.com/profile.php?do=editprofile'
    profile_sec_url=f'https://www.warriorforum.com/members/{username}.html'

    
    response = warriorforums_automation(main_email, app_pass,username,password,user_email,settings_url,profile_url,profile_sec_url, site_url)
    print(response)
    time.sleep(10)
