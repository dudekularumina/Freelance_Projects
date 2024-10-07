from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless


API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--incognito")




# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

def vimeo_automation(main_email, app_pass,fullname,user_email,profile_url, site_url):

    try:
        driver.get(site_url)
        time.sleep(5)
        
        join_btn=driver.find_element(By.XPATH,'//*[@id="root"]/section[1]/div/div[2]/ul/li[2]/button')
        join_btn.click()
        time.sleep(8)

        iframe = driver.find_element(By.CSS_SELECTOR, "iframe.sc-sml230-0.jmnrPY")
        driver.switch_to.frame(iframe)
            
        email=driver.find_element(By.CSS_SELECTOR,'#email_login')
        email.send_keys(user_email)
        time.sleep(10)
        
    
        continue_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div/div/section/form[2]/button')
        continue_btn.click()
        time.sleep(8)

        name_input=driver.find_element(By.ID,'name')
        name_input.send_keys(fullname)
        time.sleep(8)

        pwd_input=driver.find_element(By.ID,'password_login')
        pwd_input.send_keys(password)
        time.sleep(8)

        join_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div/div/section/form/section[2]/button')
        join_btn.click()
        time.sleep(10)


        # Switch back to the default content after interacting with the iframe
        driver.switch_to.default_content()

        driver.get(profile_url)
        time.sleep(8)



        about_sec=driver.find_element(By.NAME,'bio')
        driver.execute_script("arguments[0].scrollIntoView(true);", about_sec)
        about_sec.send_keys("Tell the world more about who you are, what you like to make, and what things you are interested in working on next. This will appear on the About page of your profile.")
        time.sleep(5)

        save_btn=driver.find_element(By.XPATH,'//*[@id="wrap"]/div[2]/main/div/div[1]/div[2]/div[2]/form/div[8]/fieldset/input')
        driver.execute_script("arguments[0].scrollIntoView(true);",save_btn)
        save_btn.click()
        time.sleep(5)

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
    fullname='Gaurav Thakur'
    password='Gaurav@4122'
    site_url ="https://vimeo.com/"
    profile_url='https://vimeo.com/settings/profile/general'

    

    response = vimeo_automation(main_email, app_pass,fullname,user_email,profile_url, site_url)
    print(response)
