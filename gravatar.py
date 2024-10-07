from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import imaplib
import email
from email import policy

# def decode_email_body(part):
#     # Decode the email body content here if necessary
#     charset = part.get_content_charset()
#     content_type = part.get_content_type()
#     body = part.get_payload(decode=True).decode(charset, errors='replace')
#     return body

def get_confirmation_code(email_id,password):
    try:
            
        imap = imaplib.IMAP4_SSL('pop.gmail.com')
        imap.login(email_id, password)
        imap.select('inbox')
        # Search for all emails in the inbox
        status, messages = imap.search(None, 'ALL')
        if status != 'OK':
            print("No messages found!")
            return None
        
        email_ids = messages[0].split()

        # Fetch the latest 10 emails
        latest_email_ids = reversed(email_ids[-10:])

        messages = []
        for e_id in latest_email_ids:
            _, msg_data = imap.fetch(e_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1], policy=policy.default)
                    messages.append(msg)
        confirmation_code = None
        for message in messages:
            if 'Gravatar' in message['from'] :
                confirmation_code = message['subject'].split(" ")[0]
                print(confirmation_code)
                return confirmation_code

        return confirmation_code
    except Exception as e:
        print(e)
        return None

def gravatar_automation(main_email, app_pass, user_email, display_name, about_content, site_url):
    try:  
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(site_url)

        # Wait for and click the consent button if it appears
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "g-signup-cta"))
        ).click()

        driver.find_element(By.CLASS_NAME, "form-text-input").send_keys(user_email)
        driver.find_element(By.CLASS_NAME, "form-button").click()

        time.sleep(10)

        confirmation_code = get_confirmation_code(main_email, app_pass)
        if confirmation_code is None:
            return {"status": "error", "message": "Confirmation code not found!"}

        driver.find_element(By.ID, "verification-code").send_keys(confirmation_code)

        driver.find_element(By.CLASS_NAME, "form-button").click()
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'do this later')]"))
            ).click()

        except Exception as e:
            print(e)
            print("it is not")
            return f"Error: {e}"

        about_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='About']"))
        )

        # Click the "About" section
        about_tab.click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "profile-editor__about-me-textarea").send_keys(about_content) 
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "gravatar-button-strip__vertical").click()

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
        site_url = "https://gravatar.com/"

        response = gravatar_automation(main_email, app_pass, user_email, display_name,  about_content, site_url)
        print(response)
        time.sleep(10)