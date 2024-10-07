from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.common.exceptions import ElementClickInterceptedException

from twocaptcha import TwoCaptcha
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def hotsearch_automation(password ,username,profile_url,user_email,site_url):
        
    try:
        # Open the website
        driver.get(site_url)
        
        # Click on the Register button
        register_button = driver.find_element(By.XPATH, "//a[text()='Register']")
        register_button.click()
        
        # Wait for the registration page to load
        WebDriverWait(driver, 10).until(EC.url_contains("hsforums_registration.php"))
        
        # Print the current URL
        print("Current URL:------------", driver.current_url)
        
        # Input username
        username_input = driver.find_element(By.ID, "regusername")
        username_input.send_keys(username)
        time.sleep(3)
        
        # Input password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        time.sleep(3)
        
        # Input confirm password
        password_confirm_input = driver.find_element(By.ID, "passwordconfirm")
        password_confirm_input.send_keys(password)
        time.sleep(5)
        
        # Input email
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(user_email)
        time.sleep(5)
        
        # Confirm email (Assuming it's the same as the email field)
        confirm_email_input = driver.find_element(By.ID, "emailconfirm")
        driver.execute_script("arguments[0].scrollIntoView(true);",confirm_email_input)

        confirm_email_input.send_keys(user_email)
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

        time.sleep(10)
        agree_checkbox = driver.find_element(By.XPATH, '//*[@id="cb_rules_agree"]') # Corrected the quotes
        try:
            agree_checkbox.click()
        except ElementClickInterceptedException:
            print("Click intercepted, attempting to click using JavaScript...")
            driver.execute_script("arguments[0].click();", agree_checkbox)

        time.sleep(10)
        driver.execute_script("window.scrollBy(0, 300);")


        
        # Click on the Complete Registration button
        complete_regis_btn = driver.find_element(By.XPATH, "//input[@value='Complete Registration']")
        # driver.execute_script("argument[0].scrollIntoView(true);",complete_regis_btn)
        time.sleep(10)
        # Attempt to click using WebDriver first
        try:
            complete_regis_btn.click()
        except ElementClickInterceptedException:
            print("Click intercepted, attempting to click using JavaScript...")
            driver.execute_script("arguments[0].click();", complete_regis_btn)

        time.sleep(5)


        print("Account Created..............")

        print("Current Url After Sign In----------", driver.current_url)

        
        # Navigate to profile page
        driver.get(profile_url) #updated
        time.sleep(10)
        
        print("Current URL after profile:----------------", driver.current_url)
        
        # Update homepage URL
        time.sleep(5)
        homepage_input = driver.find_element(By.ID, "tb_homepage")
        driver.execute_script("arguments[0].click();", homepage_input)

        homepage_input.send_keys("https://mysamplesite.com") #sampleurl
        time.sleep(10)
        
        # Click on "Edit Signature"
        edit_signature_link = driver.find_element(By.XPATH, "//a[text()='Edit Signature']")
        edit_signature_link.click()
        
        # Wait for the signature editing page to load
        WebDriverWait(driver, 20).until(EC.url_contains("profile.php?do=editsignature"))
        print("Current URL after clicking 'Edit Signature':----------------", driver.current_url)
        time.sleep(5)
        driver.get(driver.current_url)
        
        # Add sample URLs to the signature
        signature_textarea = driver.find_element(By.CSS_SELECTOR, "textarea.cke_source")
        time.sleep(5)

        signature_textarea.clear()
        time.sleep(8)
        #Adding sample urls
        signature_textarea.send_keys("[URL=\"http://mysite1.com\"]http://mysite1.com[/URL]\n[URL=\"http://mysite2.com\"]http://mysite2.com[/URL]")
        
        # Click on "Save Signature"
        time.sleep(8)
        save_signature_button = driver.find_element(By.CSS_SELECTOR, "input[value='Save Signature']")
        time.sleep(3)

        save_signature_button.click()
        time.sleep(3)
        
        # Click on the Profile element with the specified XPath
        top_link = driver.find_element(By.XPATH, "//*[@id='toplinks']/ul/li[3]/a")
        top_link.click()
        time.sleep(5)
        
        # Print the current URL
        print("Current URL after clicking top link:----------------", driver.current_url)
        driver.get(driver.current_url)
        time.sleep(3)
        
        # Click on the "About Me" tab
        about_me_tab = driver.find_element(By.ID, "aboutme-tab")
        about_me_tab.click()
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, 400);")
        # driver.execute_script("window.scrollBy(0, 300);")

        
        # Print the current URL
        print("Current URL after clicking 'About Me':----------------", driver.current_url)
        time.sleep(15)

            

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)


if __name__ == "__main__":
    trial_users = [{"user_email":"user7655@additivedecor.com", "username":"gaurav56544","password":"Gaurav@3455799"}, {"user_email":"user56117@additivedecor.com", "username":"Thakur5624443","password":"Thakur@352524"}]    
    
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
    
        site_url = "https://forums.hostsearch.com/"
        profile_url="https://forums.hostsearch.com/profile.php?do=editprofile"

        driver = create_driver()


        response = hotsearch_automation(password=password ,username=username,profile_url=profile_url,user_email=user_email, site_url=site_url)
        print(response)
        time.sleep(10)
