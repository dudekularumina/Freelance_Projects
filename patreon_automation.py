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
from selenium.webdriver.common.keys import Keys
import pyautogui

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


IMAP_SERVER = "imap.gmail.com" 
EMAIL_FOLDER = "inbox"  # or the folder where the confirmation email is located


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


def patreon_automation(main_email, app_pass,password ,name,cretorname,signup_url,about_url,user_email,site_url,sample_url):

        # Function to fetch the confirmation link from the email
    def get_confirmation_link():
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(main_email,app_pass)
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


    try:
        driver.get(site_url)
        time.sleep(10)

        driver.get(signup_url)
        time.sleep(10)

        email_input=driver.find_element(By.NAME,'email')
        email_input.send_keys(user_email)
        email_input.send_keys(Keys.ENTER)
        time.sleep(10)


        name_input=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div/div[1]/div/div[1]/div/div/div[1]/div/form/div[3]/div/div/div/div/input')
        name_input.send_keys(name)
        time.sleep(10)

        password_input1=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div/div[1]/div/div[1]/div/div/div[1]/div/form/div[4]/div/div/div[1]/div/div[1]/input')
        password_input1.send_keys(password)
        time.sleep(10)

        
        continue_btn2=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div/div[1]/div/div[1]/div/div/div[1]/div/form/div[5]/div/button')
        continue_btn2.click()
        time.sleep(10)
        #Google PAssword Saving Window
        pyautogui.press('enter')
        time.sleep(10) 

        cretor_name=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div[1]/form/div/div[2]/div/div/div/div/input')
        cretor_name.send_keys(cretorname)
        time.sleep(10)

        
        continue_btn2=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/div[1]/form/div/button')
        continue_btn2.click()
        time.sleep(10)
        
        continue_btn3=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/form/button')
        continue_btn3.click()
        time.sleep(10)

        skip_btn=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div[2]/div/div/form[2]/button')
        skip_btn.click()
        time.sleep(10)
        try:
            close_btn1=driver.find_element(By.CSS_SELECTOR,'#catalog-monetization-ga > div.sc-lbhJGD.dGovNZ > div > div.sc-jObWnj.gIlPzo > div.sc-hUpaCq.gyWIQw > button')
            close_btn1.click()
            time.sleep(10)
        except:
            close_btn2=driver.find_element(By.XPATH,'//*[@id="catalog-monetization-ga"]/div[2]/div/div[1]/div[1]/button')
            close_btn2.click()
            time.sleep(10)

        
        confirmation_link = get_confirmation_link()
        if confirmation_link:
                print(f"Confirmation link: {confirmation_link}")
                driver.get(confirmation_link)
                time.sleep(10)
        else:
                print("Confirmation link not found.")


        # #=======================login=============================
        # driver.get(login_url)
        # time.sleep(10)

        # email_input1=driver.find_element(By.NAME,'email')
        # email_input1.send_keys(main_email)
        # time.sleep(10)

        # continue_btn3=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div/div[1]/div/div/div/form/div[3]/button')
        # continue_btn3.click()
        # time.sleep(10)

        # password_inp=driver.find_element(By.NAME,'current-password')
        # password_inp.send_keys(password)
        # time.sleep(10)

        
        # continue_btn4=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div/div[1]/div/div/div/form/div[4]/button')
        # continue_btn4.click()
        # time.sleep(10)

        print("Current URL",driver.current_url)
        time.sleep(10)


        driver.get(about_url)
        time.sleep(10)

        about_section=driver.find_element(By.XPATH,'//*[@id="renderPageContentWrapper"]/div[1]/div/div/div/div[4]/div/div/div[1]/div/div/div[2]/div[2]/button')
        about_section.click()
        time.sleep(10)

        # Locate the contenteditable div element
        content_editable_div = driver.find_element(By.CSS_SELECTOR, "div.ProseMirror.remirror-editor")
        
        # Define the sample URL
        # sample_url = "https://www.example.com"

        # Use JavaScript to set the content of the <p> tag inside the contenteditable div
        script = f"""
        var div = arguments[0];
        var pTag = div.querySelector('p');
        if (pTag) {{
            pTag.innerHTML = 'Check out this link: <a href="{sample_url}" target="_blank">{sample_url}</a>';
        }}
        """
        driver.execute_script(script, content_editable_div)

        time.sleep(10)

        save_btn=driver.find_element(By.XPATH,'//*[@id="introduceYourselfModal"]/div[2]/div/div[2]/div/button[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);",save_btn)    
        save_btn.click()
        time.sleep(10)
        
        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}

    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    trial_users = [{"user_email":"user77744@additivedecor.com", "username":"gaurav448437","password":"Gaurav@3822355","name":"Gurav","cretorname":"Sample11","sample_url":"https://www.exampl1eurl.com"},
                   {"user_email":"user54677@additivedecor.com", "username":"thakur564747434","password":"Thakur@3675767","name":"Thakur","cretorname":"Sample22","sample_url":"https://www.example2yrl.com"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        password = trail_creds["password"]
        name=trail_creds["name"]
        cretorname=trail_creds["cretorname"]
        sample_url=trail_creds["sample_url"]


        site_url = 'https://www.patreon.com/'
        signup_url='https://www.patreon.com/create'
        login_url='https://www.patreon.com/login'
        about_url='https://www.patreon.com/user/about'

        driver=create_driver()

        response = patreon_automation(main_email, app_pass,password=password ,name=name,cretorname=cretorname,signup_url=signup_url,about_url=about_url,user_email=user_email, site_url=site_url,sample_url=sample_url)
        print(response)
        time.sleep(10)