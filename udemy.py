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


# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

def udemy_automation(main_email,app_pass,user_email,fullname,lastname,password,signup_url,profile_url,site_url):
      
    try:
        driver.get(site_url)
        time.sleep(5)

        driver.get(signup_url)
        time.sleep(10)

        fullname_input=driver.find_element(By.NAME, 'fullname')
        fullname_input.send_keys(fullname)
        time.sleep(4)

        email_input=driver.find_element(By.NAME, 'email')
        email_input.send_keys(user_email)
        time.sleep(4)

        pwd_input=driver.find_element(By.NAME, 'password')
        pwd_input.send_keys(password)
        time.sleep(5)

        signup_btn=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div[2]/div/main/div/div/form/div[6]/button')
        signup_btn.click()
        time.sleep(10)

        fields_check=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div/div/div/div/div[2]/div/div/div[2]/label[3]')
        fields_check.click()
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        mngppl_check=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div/div/div/div/div[2]/div/div/div[3]/label[2]')
        mngppl_check.click()
        time.sleep(4)

        next_btn=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div/div/div/div/div[3]/button')
        next_btn.click()
        time.sleep(4)

        next_btn1=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div/div/div/div/div[3]/button[2]')
        next_btn1.click()
        time.sleep(4)

        start_learning=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div/div/div/div/div[3]/button[2]')
        start_learning.click()
        time.sleep(5)

        print("Current URL====", driver.current_url)
        time.sleep(5)

        driver.get(profile_url)
        time.sleep(5)
    
        lastname=driver.find_element(By.NAME,'surname')
        lastname.send_keys(lastname)
        time.sleep(4)



        website_url_input=driver.find_element(By.NAME,'website_url')
        driver.execute_script("arguments[0].scrollIntoView(true);", website_url_input)

        website_url_input.send_keys('https://www.samplewebsite.com/') #Backlink
        time.sleep(4)



        save_btn=driver.find_element(By.XPATH,'//*[@id="udemy"]/div[1]/div[2]/div/div[2]/div[2]/form/div/div[3]/button')
        driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
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
    fullname='Gaurav Thakur'
    lastname='Thakur'
    password='Gaurav@412246'
    site_url = "https://www.udemy.com/"
    signup_url='https://www.udemy.com/join/signup-popup/?locale=en_US&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F'
    profile_url='https://www.udemy.com/user/edit-profile/'

    response = udemy_automation(main_email,app_pass,user_email,fullname,lastname,password,signup_url,profile_url, site_url)
    print(response)
    time.sleep(10)

