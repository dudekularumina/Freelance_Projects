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
from selenium.common.exceptions import InvalidSelectorException, TimeoutException
import random
import pyautogui
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

# Function to extract the verification link from the email
def extract_verification_link(email_body):
    soup = BeautifulSoup(email_body, 'html.parser')
    verify_link = soup.find('a', string="Verify Email")
    if verify_link:
        return verify_link.get('href')
    else:
        return None

# Recursive function to extract text from email parts
def extract_html_from_part(part):
    if part.is_multipart():
        for subpart in part.iter_parts():
            result = extract_html_from_part(subpart)
            if result:
                return result
    elif part.get_content_type() == 'text/html':
        return part.get_payload(decode=True).decode()
    return None

# Function to get the verification link from the latest email
def get_verification_link(email_id, app_password):
    try:
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()

        latest_email_id = email_ids[-1]
        _, msg_data = imap.fetch(latest_email_id, '(RFC822)')
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

        email_body = extract_html_from_part(msg)

        if email_body:
            link = extract_verification_link(email_body)
            if link:
                print("Verification link found:", link)
                return link
            else:
                print("Verification link not found in the email.")
        else:
            print("No HTML content found in the email.")
        
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to solve reCAPTCHA
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
def qualtrics_automation(main_email, app_pass,password ,firstname,lastname,signup_url,user_email, site_url):

    try:
        # Open the website
        driver.get(site_url)
        time.sleep(5)

        #======================= create account=====================
        
        driver.get(signup_url)#updated
        time.sleep(5)

        # Select the "Personal" option from the dropdown
        use_case_dropdown = Select(driver.find_element(By.ID, "use_case"))
        use_case_dropdown.select_by_value("PERSONAL")
        time.sleep(2)

        # Enter the email address
        email_input = driver.find_element(By.ID, "email")
        for char in user_email:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.3, 0.5)) 
        time.sleep(20)

        # Handle reCAPTCHA if present
        try:
            wait = WebDriverWait(driver, 10)
            try:
                time.sleep(5)
                site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                current_url = driver.current_url
                captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

                if captcha_solution:
                    driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                    print("reCAPTCHA response submitted")
            except:
                print("Image CAPTCHA not displayed.")
        except Exception as e:
            print(f"No Image CAPTCHA handling: {e}")

        # Click the "Create Account" button
        create_account_button = driver.find_element(By.ID, "q-free-account-form-submit-button")
        driver.execute_script("arguments[0].click();", create_account_button)

        time.sleep(20)

        #=====================Get the verification link from the email=======================

        verification_link = get_verification_link(main_email,app_pass)
        if verification_link:
            # Navigate to the verification link
            driver.get(verification_link)
            print("Navigating to the verification link...")
            time.sleep(5)
            print("Current URL-----------", driver.current_url)
            time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        firstname_input = driver.find_element(By.ID, "firstName")
        firstname_input.send_keys(firstname) #Gaurav
        time.sleep(3)

        lastname_input= driver.find_element(By.ID, "lastName")
        lastname_input.send_keys(lastname) 
        time.sleep(3)

        password_input= driver.find_element(By.ID, "password")
        password_input.send_keys(password) #Gaurav@4122
        time.sleep(3)
        
        confm_password = driver.find_element(By.ID, "confirmedPassword")
        confm_password.send_keys(password) #Gaurav@4122
        time.sleep(3)

        continue_btn=driver.find_element(By.XPATH, "//*[@id='app']/div/form/button")
        continue_btn.click()
        time.sleep(10)

        try:
            cancel_btn=driver.find_element(By.ID,'close-onboarding')#<button id="close-onboarding" aria-disabled="false" type="button" class="back-button--NF70j_UMSlTgnkQ _-mZir _AAJ9d">Cancel</button>
            driver.execute_script("arguments[0].click();", cancel_btn)
            
            time.sleep(10)
        except Exception as e:
            print(f"Exception occured ", {e})
            time.sleep(3)

        print("Current URL------", driver.current_url)
        time.sleep(5)

        try:
            create_project_btn1=driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div[2]/div/button')
            create_project_btn1.click()                        
            time.sleep(10)
        except Exception as e:
            print(f"Exception",e)
            time.sleep(10)
        
        try:
            close_button = driver.find_element(By.CLASS_NAME, "shepherd-cancel-icon")
            close_button.click()
        except Exception as e:
            print(f"Exception ",e)
            
        time.sleep(10)
        
        survey_btn=driver.find_element(By.XPATH, "//*[@id='root']/div[2]/div[2]/div[2]/div[1]/div[2]/div/button")
        survey_btn.click()                        #//*[@id="root"]/div[2]/div[2]/div[2]/div[1]/div[2]/div/button
        time.sleep(10)

        # try:
        #     pyautogui.press('enter')
        # except:
        #     for _ in range(2):  # Adjust the range based on how many times you need to press Tab
        #        pyautogui.press('tab')
        #        time.sleep(1)
        #     pyautogui.press('enter')

        get_started=driver.find_element(By.XPATH, "//*[@id='root']/div[2]/div[3]/div/div[3]/div/button")
        get_started.click()                        #//*[@id="root"]/div[2]/div[3]/div/div[3]/div/button
        time.sleep(10)

        # project_name=driver.find_element(By.XPATH,'//*[@id="ea66f9cc-ea33-4594-a907-17b9eddae42b"]/label/input')
        # project_name.send_keys("Sample Project")
        # time.sleep(10)

        create_project=driver.find_element(By.XPATH, "/html/body/div[12]/div[2]/div/form/div/div[2]/button[1]")
        create_project.click()
        time.sleep(15)
        try:
            skip_tour=driver.find_element(By.XPATH,'//*[@id="body"]/div[10]/div/footer/button[1]')
            skip_tour.click()
            time.sleep(20)
        except Exception as e:
            print(f"Exception ",e)

        try:        
            # Use a proper XPath to locate the "Add new question" button
            add_new_qus_btn = driver.find_element(By.XPATH, "//button[@class='footer-add-button _vnu9r _7aPNy']")
            add_new_qus_btn.click()
            time.sleep(5)
        
        except :
            add_new_qus_btn1=driver.find_element(By.CLASS_NAME, "footer-add-button")
            add_new_qus_btn1.click()
        # except TimeoutException as e:
        #     print("TimeoutException: Element not found or not clickable within the given time.")


        time.sleep(10)
        # Step 1: Click on the "Text / Graphic" option in the dropdown
        text_graphic_option = driver.find_element(By.XPATH, "//div[@id='question-type-footer-dropdown-DB']//span[contains(text(),'Text / Graphic')]")
        text_graphic_option.click()
        time.sleep(8)

        # Step 2: Click on the "Click to write the question text" area
        question_text_area =driver.find_element(By.XPATH, "(//div[@class='QuestionText' and contains(text(),'Click to write the question text')])[2]")
        question_text_area.click()
        time.sleep(5)

        run_content=driver.find_element(By.XPATH, '//*[@id="RichTextToolBar"]/div[1]/div/a[1]')
        run_content.click()
        time.sleep(8)

        # Switch to the iframe
        iframe = driver.find_element(By.XPATH, "//iframe[@class='cke_wysiwyg_frame cke_reset']")
        driver.switch_to.frame(iframe)
        time.sleep(5)

        # Locate the body inside the iframe and clear the text
        iframe_body = driver.find_element(By.XPATH, "//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")
        iframe_body.clear()
        time.sleep(5)

        # If the clear method doesn't work, try sending backspace or delete keys
        iframe_body.send_keys(Keys.CONTROL + "a")
        iframe_body.send_keys(Keys.DELETE)
        time.sleep(5)

        # Switch back to the main content to interact with the dialog
        driver.switch_to.default_content()

        
        more_opt=driver.find_element(By.ID,"cke_26")
        more_opt.click()
        time.sleep(10)
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(8)

                # Locate the button using the href attribute
        link_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:void('Link')\"]")
        link_button.click()
        time.sleep(5)

        # Enter the sample URL in the input field   //*[@id="cke_1723_textInput"]
        # Wait for the second input field to be visible
        url_input = driver.find_element(By.XPATH, "//input[@class='cke_dialog_ui_input_text' and @type='text']")
        url_input.send_keys("Sample URL")
        time.sleep(2)

        url_input = driver.find_element(By.XPATH, "(//input[@class='cke_dialog_ui_input_text' and @type='text'])[2]")
        url_input.send_keys("sampleurl")
        time.sleep(2)

        # Click the "OK" button in the dialog
        ok_button = driver.find_element(By.XPATH, "//a[@class='cke_dialog_ui_button cke_dialog_ui_button_ok']")
        ok_button.click()
        time.sleep(5)

        body = driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(5)

        # Click on the "Publish" button
        publish_button = driver.find_element(By.XPATH, "//button[@id='publish-button']")
        publish_button.click()
        time.sleep(5)

        # Click the "Publish" button in the confirmation popup
        confirm_publish_button = driver.find_element(By.XPATH, "//button[contains(@class, 'confirm-button') and contains(text(), 'Publish')]")
        confirm_publish_button.click()
        time.sleep(30)

        # Click the "Okay" button in the final confirmation
        okay_button = driver.find_element(By.XPATH, "//button[contains(@class, 'confirm-button') and contains(text(), 'Okay')]")
        okay_button.click()
        time.sleep(5)

        # Print the current URL
        print("Current URL after completion:", driver.current_url)
    
        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(20)


if __name__ == "__main__":
    trial_users = [{"user_email":"user8755568@additivedecor.com", "password":"Gaurav@8778778"},
                   {"user_email":"user45668678@additivedecor.com", "password":"Thakur@3638458"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        password = trail_creds["password"]
        firstname='Gaurav'
        lastname='Thakur'
    
        
        site_url = "https://www.qualtrics.com/"
        signup_url="https://www.qualtrics.com/free-account/"
        # login_url="https://login.qualtrics.com/login"

        driver=create_driver()

        response = qualtrics_automation(main_email, app_pass,password=password ,firstname=firstname,lastname=lastname,signup_url=signup_url,user_email=user_email,  site_url=site_url)
        print(response)
