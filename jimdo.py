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
from selenium.webdriver.common.keys import Keys
import email
from bs4 import BeautifulSoup
import re
import pyautogui




# Function to clean text by replacing problematic characters
def clean_text(text):
    return text.replace('\xa0', ' ').encode('utf-8', errors='ignore').decode('utf-8')

# Function to extract the confirmation link by matching "Confirm now" or fallback link text
def extract_link_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Clean HTML content to avoid encoding issues
    html_content = clean_text(html_content)
    
    # Try to find the 'a' tag with the "Confirm now" text
    button_link = soup.find('a', string=lambda text: "Confirm now" in text if text else False)
    
    if button_link and button_link.has_attr('href'):
        return button_link['href']
    
    # If no button found, search for the fallback text link in the email body
    fallback_link = re.search(r'(https?://[^\s]+)', html_content)
    if fallback_link:
        return fallback_link.group(0)
    
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

        # Check the subject to see if it contains "Jimdo"
        subject = msg['subject']
        if "Jimdo" in subject:
            print(f"Email Subject: {subject}")

            # Extract the link from the email
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/html':
                    # Get the correct charset of the email part if it's set
                    charset = part.get_content_charset()
                    if not charset:
                        charset = 'utf-8'  # Default to utf-8 if no charset is found
                    
                    # Decode the payload using the identified or default charset
                    html_part = part.get_payload(decode=True).decode(charset, errors='ignore')
                    
                    # Clean the HTML part before further processing
                    html_part = clean_text(html_part)
                    
                    confirmation_link = extract_link_from_html(html_part)
                    if confirmation_link:
                        print("Confirmation link found in the email.")
                        return confirmation_link
            print("Confirmation link not found in the email content.")
        else:
            print(f"No Jimdo-related email found. Email Subject: {subject}")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def create_driver():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def jimdo_automation(main_email, app_pass,password ,signup_url,user_email,link_text,link_url, site_url):

    try:
        # Open the website
        driver.get(site_url)
        time.sleep(20)
        try:       
            for _ in range(6):  # Adjust the range based on how many times you need to press Tab
                pyautogui.press('tab')
                time.sleep(1)

            # Now press Enter to click the "Accept All" button
            pyautogui.press('enter')
        except:
            print("cookies Consent Not Clicked")
        time.sleep(8)

        driver.execute_script("window.scrollBy(0, 400);")

        start_free=driver.find_element(By.XPATH,'//*[@id="hero_b"]/div[4]/div/button')
        # driver.execute_script("arguments[0].scrollIntoView(true);",start_free)
        start_free.click()
        time.sleep(10)

        driver.get(signup_url)
        # signup_email.click()                      #/html/body/div[6]/div/div/div/div[2]/div[1]/div[4]/a
        time.sleep(10)

        email_input=driver.find_element(By.ID,'email')
        email_input.send_keys(user_email)
        time.sleep(15)

        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(10)

        check_box=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[1]/div/form/div[4]/label[2]/input')
        driver.execute_script("arguments[0].scrollIntoView(true);",check_box)
        check_box.click()
        time.sleep(10)

        create_acc=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[1]/div/form/div[5]/button')
        create_acc.click()
        time.sleep(25)

        
        try:
            # Get confirmation link
            confirmation_link = get_confirmation_link(main_email,app_pass)

            if confirmation_link:
                print(f"Confirmation link: {confirmation_link}")
            else:
                print("Failed to retrieve confirmation link.")

            # Open the link with Selenium
            driver.get(confirmation_link)
            time.sleep(10)  # Wait for the confirmation process to complete

        except:
            print("Confirmation button not clicked")

        print("Current Url",driver.current_url)
        time.sleep(5)

          
        try:   
            email_input=driver.find_element(By.ID,'email')
            driver.execute_script("arguments[0].scrollIntoView(true);",email_input)

            email_input.send_keys(main_email)
            time.sleep(10)

            
            pwd_input=driver.find_element(By.ID,'password')
            driver.execute_script("arguments[0].scrollIntoView(true);",pwd_input)
            pwd_input.send_keys(password)
            time.sleep(10)

            login_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[1]/div/form/div[5]/button')
            login_btn.click()
            time.sleep(5)
        except:
            print("Exception Executed")

        time.sleep(5)
        start_now_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/button')
        start_now_btn.click()
        time.sleep(8)

        # #dashboard
        # driver.get(dashboard_url)
        # time.sleep(10)
        

        # driver.execute_script("window.scrollBy(0, 400);")
        # time.sleep(10)
        skip_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn.click()#                       //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        skip_btn1=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn1.click()#                     //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        continue_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/button[2]')
        continue_btn.click()#n                    //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/button[2]
        time.sleep(10)

        skip_btn2=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn2.click()#                     //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        skip_btn3=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn3.click()           #           //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        skip_btn4=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn4.click() #                     //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        skip_btn5=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn5.click()#                
        time.sleep(5)

        skip_btn6=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn6.click()#                      //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(5)

        # skip_btn7=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        # skip_btn7.click()
        # time.sleep(10)

        
        
        continue_btn1=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/button[2]')
        continue_btn1.click()#                      //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/button[2]
        time.sleep(8)

        skip_btn8=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button')
        skip_btn8.click()#                      //*[@id="root"]/div/div/div/div/div/div[2]/div[3]/div[2]/div/button
        time.sleep(8)

        try:                                  
            get_now=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/button')
            driver.execute_script("argumnets[0].scrollIntoView(true);",get_now)
            get_now.click()#                      //*[@id="root"]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/button
            time.sleep(8)
        except:
        
            get_now1=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/button')
            get_now1.click()#                      //*[@id="root"]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/button
            time.sleep(10)
            print("Except Excuted...................")

        try:

            start_free_acc=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/main/div/div[1]/div[2]/div[12]/button')
            start_free_acc.click()#                      //*[@id="__next"]/div/div[2]/main/div/div[1]/div[2]/div[12]/button  //*[@id="__next"]/div/div[2]/main/div/div[1]/div[2]/div[12]/button
            time.sleep(20)

            close_btn=driver.find_element(By.XPATH,'//*[@id="closeModalBtn"]')
            close_btn.click()                      #//*[@id="closeModalBtn"]
            time.sleep(0)
        except:
            print("Except Executed")

        time.sleep(10)
        # website_builder=driver.find_element(By.XPATH,'//*[@id="ia-sidebar"]/nav/div/ul/li[2]/a')
        # website_builder.click() #https://cms.jimdo.com/cms/
        # driver.get("https://cms.jimdo.com/cms/")
        # time.sleep(10)
        # 

        #=========Adding Backlink==========     
        # Locate the <p> tag (adjust this selector based on your actual DOM)
        p_element = driver.find_element(By.XPATH, "//p[@class='text-align-center']")
        driver.execute_script("arguments[0].scrollIntoView(true);",p_element)
        time.sleep(10)

        # Click on the <p> element to focus on it
        p_element.click()

        existing_text = p_element.text

        # Define the link you want to append
        
        link_html = f'{existing_text} <a href="{link_url}" target="_blank">{link_text}</a>'

        # Append the new link after the existing text in the <p> tag
        driver.execute_script("arguments[0].innerHTML = arguments[1];", p_element, link_html)

        # Optionally, wait to observe the change
     
        time.sleep(10)
        #==========================================

        publish_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div[3]/div/div/div/div[1]/div/div/div[3]/div[1]/button')
        publish_btn.click()
        time.sleep(10)

        link=driver.find_element(By.XPATH,'/html/body/div[56]/div/div/div[2]/a')
        link.click()

        
        # close_btn=driver.find_element(By.XPATH,'/html/body/div[56]/div/div/button')
        # close_btn.click()
        # time.sleep(10)
 # Wait for the content to be added

        print('Website URL',driver.current_url)
        time.sleep(10)
    

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)

if __name__ == "__main__":
    trial_users = [{"user_email":"user6762@additivedecor.com", "username":"gaurav76877","password":"Gaurav@3887876        "}, {"user_email":"user5467@additivedecor.com", "username":"Thakur564747434","password":"Gaurav@367575623"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        password = trail_creds["password"]

    
        signup_url="https://account.e.jimdo.com/signup/email"
        site_url ='https://www.jimdo.com/'

        link_text = 'Visit my website'
        link_url = 'https://www.sample.com'

        # link_text = 'sample Backlink'
        # link_url = 'https://www.sample.com'

        driver = create_driver()


        response = jimdo_automation(main_email, app_pass,password=password ,signup_url=signup_url,user_email=user_email,link_text=link_text,link_url=link_url, site_url=site_url)
        print(response) 