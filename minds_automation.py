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


def extract_code_from_subject(subject):
    code_pattern = re.compile(r'\b\d{6}\b')  # Pattern to match a 6-digit code
    match = code_pattern.search(subject)
    if match:
        return match.group(0)
    return None

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

        # Extract the subject line
        subject = msg['subject']
        print(f"Email Subject: {subject}")

        # Extract the confirmation code from the subject line
        code = extract_code_from_subject(subject)
        if code:
            print("Confirmation code found in the subject line.")
            return code
        else:
            print("Confirmation code not found in the subject line.")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def minds_automation(main_email, app_pass,password ,username,profile_url,user_email,sample_url, site_url):
    
    try:
        driver.get(site_url)
        time.sleep(10)

        join_btn=driver.find_element(By.XPATH,'/html/body/m-app/m-topbarwrapper/m-topbar/div/div/div[2]/div[3]/div[1]/m-button[2]/button')
        join_btn.click()
        time.sleep(20)

        #GauravThakur
        username_input=driver.find_element(By.ID,'username')
        username_input.send_keys(username)
        time.sleep(5)


        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(8)
        
        email_input=driver.find_element(By.ID,'email')
        email_input.send_keys(user_email)
        time.sleep(5)

    
        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(5)

        password_input2=driver.find_element(By.ID,'password2')
        password_input2.send_keys(password)
        time.sleep(5)

        check_box=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-auth__modal/div/div[1]/m-registerform/div[1]/form/div[3]/div/m-forminput__checkbox[2]/label/div/span[1]')
        check_box.click()
        time.sleep(8)

        
        join_btn1=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-auth__modal/div/div[1]/m-registerform/div[2]/m-button/button')
        join_btn1.click()
        time.sleep(20)

        

        # Retrieve the confirmation code from the email
        confirmation_code = get_confirmation_code(main_email, app_pass)

        # Enter the confirmation code in the form
        if confirmation_code:
            print("Confirmation code ",confirmation_code)
            verify_code = driver.find_element(By.ID, 'code')
            verify_code.send_keys(confirmation_code)
            time.sleep(5)
        else:
            print("Failed to retrieve the confirmation code.")

        time.sleep(5)

        continue_btn=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__verifyemailcontent/m-onboardingv5__footer/div/m-button/button')
        continue_btn.click()
        time.sleep(5)

        click_item1=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__tagselectorcontent/div/div/div[2]')
        click_item1.click()
        time.sleep(4)

        click_item2=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__tagselectorcontent/div/div/div[12]')
        click_item2.click()
        time.sleep(4)

        click_item3=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__tagselectorcontent/div/div/div[19]')
        click_item3.click()
        time.sleep(8)

        continue_btn1=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__tagselectorcontent/m-onboardingv5__footer/div/m-button/button')
        continue_btn1.click()
        time.sleep(5)

        check_box1 = driver.find_element(By.ID, 'discover_communities')  
        check_box1.click()
        time.sleep(5)

        
        continue_btn2=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__radiosurveycontent/m-onboardingv5__footer/div/m-button/button')
        continue_btn2.click()
        time.sleep(8)

        
        skip_btn=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__channelrecommendationscontent/m-onboardingv5__footer/div/m-button/button')
        skip_btn.click()
        time.sleep(8)

        
        skip_btn1=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-onboardingv5modal/m-onboardingv5/div/div[1]/m-onboardingv5__channelrecommendationscontent/m-onboardingv5__footer/div/m-button/button')
        skip_btn1.click()
        time.sleep(10)
        
        close_img=driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/m-upgradepage/m-modalclosebutton/a')
        close_img.click()
        time.sleep(10)

        driver.get(profile_url)
        time.sleep(10)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(10)

        post_btn=driver.find_element(By.XPATH,'/html/body/m-app/m-page/m-body/div/div/m-channel-container/m-channel-v2/div/m-channel__content/div/m-channel__feed/div/div[1]/div[3]/m-button/button')
        post_btn.click()
        time.sleep(8)

                        # Locate the textarea element using its unique ID
        textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Speak your mind...']"))
        )

                # Use JavaScript to set the value of the textarea with the link
        # sample_url = "https://your-link.com"
        driver.execute_script("arguments[0].value = arguments[1];", textarea, sample_url)

        # Optionally, dispatch an input event to simulate user typing (if needed)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", textarea)

        time.sleep(30)  # Pause to observe the changes
        try:
            # Locate the "Post" button using its text and click it
            post_button = driver.find_element(By.XPATH, "//span[text()='Post']/ancestor::button")
            post_button.click()
            print("Posted............")

        except:
            post_button1 = driver.find_element(By.CSS_SELECTOR, "button.m-button--blue[type='submit']")
            post_button1.click()
            print("Posted........")


    
        time.sleep(10)

        print("Current URL===", driver.current_url)
        time.sleep(10)


        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)

if __name__ == "__main__":
    trial_users = [{"user_email":"user56657@additivedecor.com", "username":"Gaurav89867853","password":"Gaurav@59887762","sample_url":"https://www.sample111.com"}, 
                   {"user_email":"user36987@additivedecor.com", "username":"Thakur58575049","password":"Thakur@49687656","sample_url":"https://www.sample222.com"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        password = trail_creds["password"]
        sample_url = trail_creds["sample_url"]
    
        site_url ='https://www.minds.com/'
        profile_url=f'https://www.minds.com/{username}/'

        driver=create_driver()

        response = minds_automation(main_email, app_pass,password=password ,username=username,profile_url=profile_url,user_email=user_email, sample_url=sample_url, site_url=site_url)
        print(response)
        time.sleep(10)