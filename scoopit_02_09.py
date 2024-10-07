from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
solver = hCaptchaProxyless()
solver.set_key(API_KEY)


EMAIL = "gauravthakur81711296@gmail.com"
PASSWORD = "ceaj vinr bkvv tpux"



# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

  
try:
    driver.get('https://www.scoop.it/')
    time.sleep(10)

    cookies_btn=driver.find_element(By.ID,'tarteaucitronPersonalize2')
    cookies_btn.click()
    time.sleep(6)

    driver.get('https://www.scoop.it/subscribe?&token=&sn=&showForm=true')
    time.sleep(5)

    fullname=driver.find_element(By.NAME,'displayName')
    fullname.send_keys("Gaurav Thakur")
    time.sleep(5)

    email_input=driver.find_element(By.NAME,'email')
    email_input.send_keys(EMAIL)
    time.sleep(5)

    password="Gaurav@4122"

    password_input=driver.find_element(By.NAME,'password')
    driver.execute_script("arguments[0].scrollIntoView(true);",password_input)
    password_input.send_keys(password)
    time.sleep(5)

    #======================Image Upload============

    # # Click the 'Upload' button to open the file upload dialog
    # upload_button = driver.find_element(By.ID, 'upload-image-button')
    # upload_button.click()
    # time.sleep(5)

    # # Instead of the upload button, locate the hidden input[type='file'] and upload an image
    # file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    # file_input.send_keys('C:/Users/MA/Desktop/Freelance_Projects/image.png')
    # time.sleep(5)
    

    # Select the dropdown option
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'job'))
    )
    select = Select(select_element)
    select.select_by_visible_text('Education')
    time.sleep(5)

 # Locate CAPTCHA element
    captcha_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="g-recaptcha"]'))
    )
    time.sleep(5)
    
    # Extract the sitekey
    sitekey = captcha_element.get_attribute('data-sitekey')
    time.sleep(3)
    
    # Setup Anti-Captcha task
    solver.set_website_url(driver.current_url)
    solver.set_website_key(sitekey)
    time.sleep(3)
    
    # Create task
    post_data = {
        'websiteURL': driver.current_url,
        'websiteKey': sitekey
    }
    task_id = solver.create_task(post_data)
    time.sleep(3)
    
    # Wait for the solution
    solution = solver.wait_for_result()

    # Wait until the CAPTCHA response element is present
    response_element_id = "h-captcha-response-07tdzavio80k"
    # WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.ID, 'h-captcha-response-07tdzavio80k'))
    # )
    time.sleep(5)
    # Fill in the CAPTCHA response
    driver.execute_script(f'document.getElementById("{response_element_id}").value = "{solution}";')




    signup_btn=driver.find_element(By.XPATH,'//*[@id="subscriptionForm"]/div[10]/div/div/button')
    signup_btn.click()
    time.sleep(6)


finally:
    time.sleep(5)
    driver.quit()