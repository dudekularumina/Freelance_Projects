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
    
def theverge_automation(email_id,email_password,site_url):

    try:
        driver.get(site_url)
        time.sleep(2)

        # Wait for the "Confirm My Choices" button and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        print("Cookies consent button clicked.")

        # Open the TED sign-up page
        driver.get("https://auth.voxmedia.com/login?community_id=671&return_to=https%3A%2F%2Fauth.voxmedia.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.theverge.com%252Fapi%252Fauth%252Fcallback%26state%3DCWgzwlkEQKtbXSpY%26client_id%3D249dc0e37d9ebca7f5848f19a0b7ea2acc2bc6dbe9acaf4da28b941e722c7048")
        time.sleep(5)

        signup_url=driver.find_element(By.XPATH,'//*[@id="auth"]/div/nav/ul/li[2]/a')
        signup_url.click()
        time.sleep(8)

        username='gauravthakur4122'
        username_input=driver.find_element(By.NAME, 'username')
        username_input.send_keys(username)
        time.sleep(5)
    
        password=driver.find_element(By.NAME, 'password')
        password.send_keys("Gaurav@4122")
        time.sleep(5)
    
        email=driver.find_element(By.NAME, 'email')
        email.send_keys(email_id)
        time.sleep(5)

        signup_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"].p-button')
        # Click the signup button
        signup_button.click()
        time.sleep(10)

        
        
        # Handle reCAPTCHA
        try:
            wait = WebDriverWait(driver, 10)

            iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
            driver.switch_to.frame(iframe)
            print("Switched to reCAPTCHA iframe")
            time.sleep(2)

            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
            recaptcha_checkbox.click()
            print("reCAPTCHA checkbox clicked")
            time.sleep(2)

            driver.switch_to.default_content()
            print("Switched back to default content")
            time.sleep(3)

            # Solve reCAPTCHA
            try:
                time.sleep(5)

                site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                current_url = driver.current_url
                captcha_solution = solve_recaptcha(API_KEY, site_key, current_url)

                if captcha_solution:
                    driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
                    print("reCAPTCHA response submitted")
            except:
                print("Failed to solve image reCAPTCHA")
                

        except Exception as e:
            print(f"CAPTCHA handling failed: {e}")

        
        signup=driver.find_elements(By.XPATH, '//*[@id="auth"]/div/form/fieldset/input')
        signup.click()
        time.sleep(20)

        driver.get(f'https://www.theverge.com/users/{username}/edit_profile')
        time.sleep(5)

        website_name=driver.find_element(By.NAME,'network_membership[website_name]')
        website_name.send_keys("sample")
        time.sleep(5)

        website_url=driver.find_element(By.NAME, 'network_membership[website_url]')
        website_url.send_keys("www.sample.com")
        time.sleep(8)

        update_btn=driver.find_element(By.XPATH,'//*[@id="submit-bar-form"]/input')
        update_btn.click()
        time.sleep(5)

        print("Current URL======", driver.current_url)
        time.sleep(5)



        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url ="https://www.theverge.com/"

    response = theverge_automation(email_id, email_password,  site_url)
    print(response)