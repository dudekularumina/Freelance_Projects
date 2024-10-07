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

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
solver = hCaptchaProxyless()
solver.set_key(API_KEY)

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--incognito")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


def solve_hcaptcha(site_key, url):
    solver = hCaptchaProxyless()
    solver.set_key(API_KEY)
    solver.set_website_url(url)
    solver.set_website_key(site_key)

    solution = solver.solve_and_return_solution()
    if solution != 0:
        print("hCaptcha solved successfully:", solution)
        return solution
    else:
        print("hCaptcha solving failed:", solver.error_code)
        return None
def evernote_automation(main_email, app_pass,password ,username,web_url,user_email, display_name,  about_content, site_url):

    try:
        # Open the website
        driver.get(site_url)
        time.sleep(10)

        close_cookie_btn=driver.find_element(By.CSS_SELECTOR,'#__next > div > div.fixed.inset-0.z-\[55\].flex.h-full.w-full.items-center.justify-center.bg-grey-10.bg-opacity-10 > div > div.flex.w-full.items-center.justify-between.bg-black.px-4.py-4.text-white > button')
        close_cookie_btn.click()
        time.sleep(15)

        try:
            close_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[1]/svg')
            close_btn.click()
            time.sleep(10)

        except:
            print("No button Present ")

        time.sleep(10)

        try:
            work_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]')
            work_btn.click()
            time.sleep(8)

            manage_btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[2]')
            manage_btn.click()
            time.sleep(8)

            btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]')
            btn.click()
            time.sleep(10)
        except:
            print("Except block Executed")

        start_free=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/section[1]/div/div[1]/a')
        start_free.click()
        time.sleep(20)

        email_login = driver.find_element(By.ID,'email')
        email_login.send_keys(main_email)
        time.sleep(15)

        continue_btn=driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div[2]/form/button')
        continue_btn.click()
        time.sleep(20)

        
        password_input=driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div[2]/form/div[1]/div/input')
        password_input.send_keys(password)
        time.sleep(20)

        
        continue_btn1=driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div[2]/form/button')
        continue_btn1.click()
        time.sleep(20)


        # Detect hCaptcha iframe and solve it
        try:
            captcha_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Main content of the hCaptcha challenge']"))
            )
            driver.switch_to.frame(captcha_iframe)
            print("hCaptcha iframe detected")

            # Get the site key
            site_key = driver.find_element(By.XPATH, '//div[@class="h-captcha"]').get_attribute("data-sitekey")
            print(f"Site key: {site_key}")

            # Solve the hCaptcha
            solution = solve_hcaptcha(site_key, driver.current_url)
            
            if solution:
                # Inject the hCaptcha solution
                driver.switch_to.default_content()
                driver.execute_script(f'document.getElementById("h-captcha-response").value="{solution}";')
                print("hCaptcha solution injected")

                # Click continue to submit the form
                continue_btn2 = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[2]/form/button')
                continue_btn2.click()
                time.sleep(10)

        except Exception as e:
            print(f"hCaptcha not detected or error: {e}")



        continue_btn2=driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div[2]/form/button')
        continue_btn2.click()
        time.sleep(20)

        continue_btn3=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div/div[2]/div/div/button')
        continue_btn3.click()
        time.sleep(15)

        work_btn1=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div/div[2]/div/div/button[2]')
        work_btn1.click()
        time.sleep(5)

        
        manage_works_btn=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div/div[2]/div/div/button[3]')
        manage_works_btn.click()
        time.sleep(5)

        online_btn=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div/div[2]/div/div/button[2]')
        online_btn.click()
        time.sleep(5)

        skip_btn=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div[1]/button')
        skip_btn.click()
        time.sleep(20)

        # continue_free=driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div/footer/div/div[1]/div/button')
        # continue_free.click()
        # time.sleep(5)

        driver.get(web_url)  #updated
        time.sleep(5)

        create_note=driver.find_element(By.XPATH,'//*[@id="qa-NAV"]/div/ul/li[2]/div[3]/div/div/div[1]/button[1]')
        create_note.click()
        time.sleep(5)


        # Switch to the iframe that contains the note editor
        editor_iframe = driver.find_element(By.XPATH, '//*[@id="qa-COMMON_EDITOR_IFRAME"]')
        driver.switch_to.frame(editor_iframe)

        # Enter title as 'Sample Note'
        title_box = driver.find_element(By.XPATH, '//*[@aria-label="Note Editor"]')
        title_box.clear()
        title_box.send_keys('Sample Note')

        # Enter the sample URL 'www.sample.com' in the body
        text_box = driver.find_element(By.XPATH, '//*[@aria-label="Note Editor"]')
        text_box.send_keys('www.sample.com')

        # Switch back to the main content after editing the note
        driver.switch_to.default_content()
    

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
    web_url='https://www.evernote.com/client/web'
    site_url = 'https://evernote.com/'

    response = evernote_automation(main_email, app_pass,password ,username,web_url,user_email, display_name,  about_content, site_url)
    print(response)