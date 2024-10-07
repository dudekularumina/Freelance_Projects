from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random


# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
# solver = hCaptchaProxyless()
# solver.set_key(API_KEY)

EMAIL = "gauravthakur81711296@gmail.com"    #gauravthakur81711296
PASSWORD = "ceaj vinr bkvv tpux"
IMAP_SERVER = "imap.gmail.com" 


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument(f"user-agent={USER_AGENT}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

try:
    driver.get('https://www.own-free-website.com/')
    time.sleep(10)


    cookies_btn=driver.find_element(By.XPATH,'//*[@id="cookieConsentAllow"]')#selector: #cookieConsentAllow
    cookies_btn.click()
    time.sleep(5)
    # try:
    get_started=driver.find_element(By.XPATH,'//*[@id="__next"]/main/section/div/div/div[1]/div[1]/a/button')
    get_started.click()
    time.sleep(10)
#     # except:
# # 
#         get_started=driver.find_element(By.CSS_SELECTOR,'#__next > main > section > div > div > div.grid.gap-0.grid-cols-1.sm\:grid-cols-2.md\:grid-cols-7.pt-6.md\:py-20.sm\:pb-\[60px\].xs\:pb-\[40px\].sm\:min-w-\[540px\].md\:mr-\[-35px\] > div.md\:py-4.max-sm\:pb-10.md\:col-span-3.flex.flex-col.max-sm\:items-center > a > button')
#         get_started.click()
#         time.sleep(10)

    email_input=driver.find_element(By.NAME,'email')
    email_input.send_keys(EMAIL)
    time.sleep(10)

    password='Gaurav@4122'
    password_input=driver.find_element(By.NAME,'password')
    password_input.send_keys(password)
    time.sleep(10)

    create_acc=driver.find_element(By.XPATH,'//*[@id=":r2:"]')##\:r2\:
    create_acc.click()
    time.sleep(10)

    text_area=driver.find_element(By.XPATH,'//*[@id=":r0:"]')
    text_area.send_keys('This is the sample website for which to sell my products online')
    time.sleep(10)

    next_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/main/div/div/form/div[3]/button')
    next_btn.click()
    time.sleep(10)

    websiite_name=driver.find_element(By.CSS_SELECTOR,'#\:r1\:')
    websiite_name.send_keys('sample')
    time.sleep(10)

    
    next_btn1=driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/main/div/div/form/div/div[2]/button')
    next_btn1.click()
    time.sleep(10)

    click_website=driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/main/div/div[2]/div[1]/div/div/div[2]/div/div/div/div[2]')
    click_website.click()
    time.sleep(10)

    
    next_btn2=driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/main/div/div[2]/div[2]/button')
    next_btn2.click()
    time.sleep(10)

    print("Current URL",driver.current_url)
    time.sleep(6)














finally:
    time.sleep(10)
    driver.quit()