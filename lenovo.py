from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re

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

# Function to extract the confirmation link from the text
def extract_link_from_text(text):
    url_pattern = re.compile(r'https://account\.lenovo\.com/us/en/account/register/verify\.html\?[^\s"]+')
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

        # Check the subject to see if it contains "Lenovo"
        subject = msg['subject']
        if "Lenovo" in subject:
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
            print(f"No Lenovo-related email found. Email Subject: {subject}")

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def lenovo_automation(main_email, app_pass, user_email,password,firstname,lastname,register_url, site_url):

    try:
        #==================================== Register on Lenovo website======================================
        driver.get(site_url)
        time.sleep(3)
        driver.get(register_url) #updated
        time.sleep(5)

        email_input = driver.find_element(By.ID, "uEmail")
        email_input.send_keys(user_email)
        time.sleep(3)

        firstname_input = driver.find_element(By.ID, "uFname")
        firstname_input.send_keys(firstname)
        time.sleep(3)

        lastname_input = driver.find_element(By.ID, "uLname")
        lastname_input.send_keys(lastname)
        time.sleep(3)

    
        pwd_input = driver.find_element(By.ID, "upwd")
        pwd_input.send_keys(password)
        time.sleep(5)

        pwd_input1 = driver.find_element(By.ID, "cpwd")
        pwd_input1.send_keys(password)
        time.sleep(5)

        # Scroll to the top of the page after entering the confirm password field
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)

        # Scroll down to the privacy checkbox or submit button (use the appropriate element)
        element = driver.find_element(By.CLASS_NAME, "agreePrivacy_checkbox")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(3)

        agree_box = driver.find_element(By.CLASS_NAME, "agreePrivacy_checkbox")
        agree_box.click()
        time.sleep(5)

        # Click the submit button
        submit_button = driver.find_element(By.XPATH, '//*[@id="fcd6ebf7-579a-411e-bb19-8dffd8bdbd49"]/main/div[3]/form/div[3]/input[2]')
        submit_button.click()
        time.sleep(20)     #Wait to load and sending the Email from 

        # Try to get the confirmation link from the email
        confirmation_link = get_confirmation_link(main_email, app_pass)
        time.sleep(5)
        
        if confirmation_link:
            # Print the confirmation link
            print(f"Confirmation Link: {confirmation_link}")

            # Open the confirmation link in the browser
            driver.get(confirmation_link)
            time.sleep(5)  # Wait for the activation page to load

                # Click the "Continue" button
            continue_button = driver.find_element(By.ID, "continueBtn")

            # Scroll to the "Continue" button
            driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
            time.sleep(3)  # Optional: wait for smooth scrolling

            # Remove the 'disabled' attribute if the button is disabled
            driver.execute_script("arguments[0].removeAttribute('disabled');", continue_button)

            # Click the "Continue" button
            continue_button.click()
            time.sleep(3)  # Wait for the next page to load

            # Print the current URL
            print(f"Current URL after clicking 'Continue': {driver.current_url}")

            time.sleep(5)

            #=============================Sign In Page and go to the Profile ===============================
            driver.get(driver.current_url)
            email_input=driver.find_element(By.ID, "emailAddress")
            email_input.send_keys(main_email)
            time.sleep(4)

            password_input=driver.find_element(By.ID, "password")
            password_input.send_keys(password)
            time.sleep(4)

            # Find the Sign In button using CSS selector for class
        
            btn_submit = driver.find_element(By.CSS_SELECTOR, ".button_disabled_button_primary.signIn")
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView();", btn_submit)  # Scroll to button
            time.sleep(2)  # Wait for smooth scrolling
            btn_submit.click()
            time.sleep(5)
        
            print(f"Current URL after clicking SignIn: {driver.current_url}")
            time.sleep(10)
            
            

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        time.sleep(10)
        driver.quit()

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

        site_url = "https://www.lenovo.com/"
        register_url="https://account.lenovo.com/us/en/account/register/register.html?orgRef=https%253A%252F%252Fwww.google.com%252F"
    
        driver=create_driver()

        response = lenovo_automation(main_email, app_pass,user_email=user_email,password=password ,firstname=firstname,lastname=lastname,register_url=register_url, site_url=site_url)
        print(response)


