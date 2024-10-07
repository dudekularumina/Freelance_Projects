from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import imaplib
import re
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import pyautogui

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
solver = hCaptchaProxyless()
solver.set_key(API_KEY)




# Define your user agent string
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"



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

def solve_recaptcha(site_key, url):
    # Step 1: Send CAPTCHA for solving
    captcha_id = requests.post('http://2captcha.com/in.php', {
        'key': API_KEY,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': url
    }).text.split('|')[1]

    # Step 2: Wait for the CAPTCHA to be solved
    time.sleep(20)  # Wait time before checking
    while True:
        res = requests.get(f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}').text
        if 'CAPCHA_NOT_READY' in res:
            time.sleep(5)  # Wait before retrying
            continue
        else:
            return res.split('|')[1]  # This is the solved CAPTCHA response


# Function to extract the confirmation link using regex
def extract_link_with_regex(content):
    # Regex pattern to match the Medium confirmation link
    pattern = r'https://medium\.com/m/callback/email\?token=[a-zA-Z0-9]+&operation=register&state=medium'
    match = re.search(pattern, content)
    if match:
        return match.group(0)
    return None

# Function to get the confirmation link from the email
def get_confirmation_link(email_id, app_password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')

        # Search for emails with "Medium" in the subject
        status, messages = imap.search(None, '(SUBJECT "Medium")')
        email_ids = messages[0].split()
        
        if not email_ids:
            print("No Medium-related emails found.")
            return None
        
        # Fetch the latest Medium email
        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        
        # Parse the email
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
        
        # Extract content from the email
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/html' or part.get_content_type() == 'text/plain':
                email_content = part.get_payload(decode=True).decode()
                confirmation_link = extract_link_with_regex(email_content)
                if confirmation_link:
                    print("Confirmation link found in the email.")
                    return confirmation_link
        
        print("Confirmation link not found in the email content.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to enter email slowly
def enter_email_slowly(driver, email, email_input):
    for char in email:
        
        email_input.send_keys(char)
        # Random delay between keystrokes to mimic human typing
        time.sleep(random.uniform(0.5, 0.8)) 

def medium_automation(main_email, app_pass,new_story_url,user_email,sample_title,sample_url, site_url):

    try:
        driver.get(site_url)
        time.sleep(10)

        get_started=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[1]/div[1]/div/div/div/div[3]/div[5]/span/a/button')
        get_started.click()
        time.sleep(7)

        signup_email=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div/div[2]/div[3]/button')
        signup_email.click()
        time.sleep(8)

        email_input=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/span/div/div/input')
        email_input.clear()
        for char in user_email:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.5, 0.8)) 
        # enter_email_slowly(driver, user_email, email_input)
        time.sleep(8)

        continue_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[3]/button')
        driver.execute_script("arguments[0].click();",continue_btn)
        # continue_btn.click()                      #   /html/body/div[2]/div/div/div/div[1]/div/div[2]/div/div[3]/button
        time.sleep(8)

        # Check if the CAPTCHA error message appears
        try:
            # Wait for the error message to appear
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.cq.b.fb.cs.jh.m.iu'))
            )
            print("reCAPTCHA message detected.")

            email_input=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/span/div/div/input')
            email_input.clear()
            for char in user_email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.5, 0.8)) 

            continue_btn1 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[3]/button')
            driver.execute_script("arguments[0].click();", continue_btn1)

            time.sleep(10)

        except Exception as e:
            print("No reCAPTCHA message found. Continuing...")
            print(f"Exception: {e}")

        okay_btn=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/div/button')
        okay_btn.click()
        time.sleep(10)

        confirmation_link = get_confirmation_link(main_email, app_pass)
        if confirmation_link:
            driver.get(confirmation_link)
            time.sleep(10)
        else:
            time.sleep(15)
            driver.quit()

        print("Current URL",driver.current_url)
        time.sleep(5)
        try:       

        # Locate the "Create Account" button using Selenium ##_obv\.shell\._surface_1727084062687 > div > div.u-minHeight100vh.u-height100pct.u-backgroundWhite.u-backgroundNoRepeat.u-flexCenter.u-justifyContentCenter > div > section > div > div > form > button
            create_account = driver.find_element(By.CSS_SELECTOR, '#_obv\.shell\._surface_1727084062687 > div > div.u-minHeight100vh.u-height100pct.u-backgroundWhite.u-backgroundNoRepeat.u-flexCenter.u-justifyContentCenter > div > section > div > div > form > button')
            driver.execute_script("arguments[0].click();", create_account) #//*[@id="_obv.shell._surface_1727084062687"]/div/div[3]/div/section/div/div/form/button
            time.sleep(10)
        except:
            for _ in range(2):  # Adjust the range based on how many times you need to press Tab
                pyautogui.press('tab')
                time.sleep(1)

            # Now press Enter to click the "Accept All" button
            pyautogui.press('enter')
            # print("Create Account Button  Not Clicked")
        time.sleep(10)

        # for i in range(6):  # Adjust the range based on how many times you need to press Tab
        #     pyautogui.press('tab')
        #     time.sleep(1)
        #     if i in (2, 3, 4, 5):  # Check for 2, 3, 4, and 5
        #         pyautogui.press('enter')

        click1=driver.find_element(By.CSS_SELECTOR,'#root > div > div.l.c > div.s.q.be.bf > div.bg.bh.l > div > div > div.by.bz.ca.cb.cc.l > div > div:nth-child(1) > div > button')
        click1.click()                             #//*[@id="root"]/div/div[3]/div[2]/div[1]/div/div/div[3]/div/div[1]/div/button
        time.sleep(5)

        click2=driver.find_element(By.CSS_SELECTOR,'#root > div > div.l.c > div.s.q.be.bf > div.bg.bh.l > div > div > div.by.bz.ca.cb.cc.l > div > div:nth-child(2) > div > button')
        click2.click()                          #//*[@id="root"]/div/div[3]/div[2]/div[1]/div/div/div[3]/div/div[2]/div/button
        time.sleep(5)

        click3=driver.find_element(By.CSS_SELECTOR,'#root > div > div.l.c > div.s.q.be.bf > div.bg.bh.l > div > div > div.by.bz.ca.cb.cc.l > div > div:nth-child(3) > div > button')
        click3.click()                        #     //*[@id="root"]/div/div[3]/div[2]/div[1]/div/div/div[3]/div/div[3]/div/button
        time.sleep(5)

        try:
            continue_btn2=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[2]/div[2]/div[2]/div/div/a')
            # continue_btn2.click()                  ##root > div > div.l.c > div.s.q.be.bf > div.aw.s.be.m.ct > div.cw.aw.l.c > div > div > a
            driver.execute_script("arguments[0].click();",continue_btn2)
            time.sleep(6)
        except:
            for _ in range(1):  # Adjust the range based on how many times you need to press Tab
                pyautogui.press('tab')
                time.sleep(1)
            pyautogui.press('enter')
        time.sleep(10)

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        try:
            free_acc=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/a')
            free_acc.click()
            time.sleep(6)
             
        except:
            free_acc=driver.find_element(By.CSS_SELECTOR,'#root > div > div.l.c > div.ir.aw.l.bf > a')
            free_acc.click()
            time.sleep(6)
            
            # driver.execute_script("arguments[0].scrollIntoView(true);",free_acc)
        

        driver.get(new_story_url) #updated
        time.sleep(7)

        # close_btn1=driver.find_element(By.CSS_SELECTOR,'#_obv\.shell\._surface_1727085695833 > div > div.drawer.u-textAlignCenter.js-drawer > button')
        # close_btn1.click()
        # time.sleep(10)

        title_span = driver.find_element(By.XPATH, '//*[@id="editor_7"]/section/div[2]/div/h3/span')
        title_span.click()
        time.sleep(10)
        title_span.clear()    
        title_span.send_keys(sample_title)

        time.sleep(6)  # Wait for a moment to ensure the title is entered

        # Locate the 'Tell your story…' span inside the p tag
        link_html = f'<a href="{sample_url}" target="_blank">{sample_url}</a>'
        story_span = driver.find_element(By.XPATH, '//*[@id="editor_7"]/section/div[2]/div/p/span')
        story_span.click()
        time.sleep(10)
        story_span.clear()
        # Inject the sample URL as a clickable link using JavaScript
        driver.execute_script("""
            var storySpan = arguments[0];
            storySpan.innerHTML = arguments[1];
            """, story_span, link_html)

        time.sleep(5)  

        # # Input the title
        # title_element = driver.find_element(By.XPATH, '//section[@name="1203"]//p[@name="e653"]')
        # # title_element.click()  
        # title_element.clear()  # Clear existing text if needed
        # title_element.send_keys(sample_title)

        # # Input the paragraph text
        # para_element = driver.find_element(By.XPATH, '//p[@name="ce11"]')
        # para_element.click()  # Click to focus if necessary
        # para_element.clear()  # Clear existing text if needed
        # para_element.send_keys(sample_url)
        # try:
        #     for _ in range(1):  # Adjust the range based on how many times you need to press Tab
        #         pyautogui.press('tab')
        #         time.sleep(1)

        #         # Now press Enter to click the "Accept All" button
        #     pyautogui.press('enter')
        # except:
        #     print("Close btn not clicked")
        
        try:
            publish_btn1=driver.find_element(By.XPATH,'//button[@data-action="show-prepublish"]')
            publish_btn1.click()
            time.sleep(10)  
        except Exception as e:
            # publish_btn1=driver.find_element(By.XPATH,'//*[@id="_obv.shell._surface_1727087591332"]/div/div[2]/div[2]/div[2]/div[1]/button')
            print(f"exception",e)
            time.sleep(8)

        time.sleep(10)

        try:
            publish_now_btn1=driver.find_element(By.XPATH,'//button[@data-action="publish"]')
            publish_now_btn1.click()
            time.sleep(15)
            print("Story Published...........")


        except Exception as e:   
            print(f"exception",e)

            
        time.sleep(10)
        try:
            close_btn=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div[2]/button')
            close_btn.click()
            time.sleep(10)
        except:
            close_btn1=driver.find_element(By.XPATH,'//button[@data-testid="publishSuccessCloseButton"]')
            close_btn1.click()
            time.sleep(10)
        print("Current URl",driver.current_url)
        

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)

if __name__ == "__main__":
    trial_users = [{"user_email":"user543995@additivedecor.com", "username":"gaurav768777","sample_title":"Sample11","sample_url":"https://www.sample111.com"}, 
                   {"user_email":"user76589@additivedecor.com", "username":"Thakur564747","sample_title":"Sample22","sample_url":"https://www.sample222.com"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        sample_title = trail_creds["sample_title"]
        sample_url=trail_creds["sample_url"]

 
        site_url ="https://medium.com/"
        new_story_url='https://medium.com/new-story'

        driver=create_driver()


        response = medium_automation(main_email, app_pass,new_story_url=new_story_url,user_email=user_email,sample_title=sample_title,sample_url=sample_url, site_url=site_url)
        print(response)
