from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import random

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
def myspace_automation(password ,username,fullname,zip_code,signup_url,login_url,profile_edit_url,user_email, site_url):


    try:
        # Open the website
        driver.get(site_url)
        
        # Accept cookies if present
        try:
            wait = WebDriverWait(driver, 10)
            accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept All Cookies']")))
            accept_cookies_button.click()
            print("Accepted cookies.")
        except Exception as e:
            print(f"No cookies banner found or error occurred: {e}")

        #===================== Proceed to the signup page============================


        driver.get(signup_url)#updated
        
        email_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "email_170")))
        email_login.click()
        time.sleep(10)
        
        # Fill in the registration details
        fullname_input = driver.find_element(By.ID, "signupEmailFullName")
        for char in fullname:
            fullname_input.send_keys(char)
            time.sleep(random.uniform(0.4, 0.6)) 
        time.sleep(8)
        
        
        username_input = driver.find_element(By.ID, "signupEmailUsername")
        for char in username:
            username_input.send_keys(char)
            time.sleep(random.uniform(0.4, 0.6)) 
        time.sleep(8)
    
        
        email_input = driver.find_element(By.ID, "signupEmailEmail")
        for char in user_email:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.4, 0.6)) 
        time.sleep(8)

            
        zip_input = driver.find_element(By.ID, "signupEmailZipcode")
        zip_input.send_keys(zip_code)
        time.sleep(3)
        
        # Select gender (Male) from the dropdown
        gender_select = Select(driver.find_element(By.ID, "signupEmailGender"))
        gender_select.select_by_visible_text("Male")
        time.sleep(3)
        
        # Input password
        password_input = driver.find_element(By.ID, "signupEmailPassword")
        password_input.send_keys(password)
        time.sleep(3)

        # Enter birth date details
        month_input = driver.find_element(By.ID, "signupEmailDobMonth")
        month_input.send_keys("06")
        time.sleep(3)
        
        day_input = driver.find_element(By.ID, "signupEmailDobDay")
        day_input.send_keys("10")
        time.sleep(3)
        
        year_input = driver.find_element(By.ID, "signupEmailDobYear")
        year_input.send_keys("1999")
        time.sleep(3)

        
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

            # Solve reCAPTCHA
            try:

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

        # Example: Closing an overlay if present
        try:
            overlay = driver.find_element(By.ID, "overlay-id")
            driver.execute_script("arguments[0].style.display = 'none';", overlay)
        except Exception as e:
            print(f"No overlay found or error occurred: {e}")

        # Now attempt to click
        tos_checkbox = driver.find_element(By.XPATH, "//*[@id='signupEmailForm']/footer/div/input")
        driver.execute_script("arguments[0].click();", tos_checkbox)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")


        
        # Click on the "Create Account" button
        time.sleep(5)
        create_account_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][form="signupEmailForm"]')
        try:
            create_account_button.click()
        except ElementClickInterceptedException:
            print("Click intercepted, attempting to click using JavaScript...")
            driver.execute_script("arguments[0].click();", create_account_button)

        print("Account Created..............")
        time.sleep(15)


        #=====================Login Page===========================

        # driver.get(login_url)#updated

        time.sleep(10)

        email=driver.find_element(By.XPATH,'//*[@id="login.email"]')
        email.send_keys(user_email)
        time.sleep(10)

        password=driver.find_element(By.XPATH, '//*[@id="login.password"]')
        password.send_keys(password)
        time.sleep(10)

        submit=driver.find_element(By.XPATH, '//*[@id="signInForm"]/footer/button')
        submit.click()
        time.sleep(10)

        #==================================================================



        print("Current URL after login,, :", driver.current_url)

        driver.get(profile_edit_url)#updated
        time.sleep(10)
    
        edit_button=driver.find_element(By.ID, "settings_editProfile")
        time.sleep(5)
        edit_button.click()
        time.sleep(5)
        print("Current URL after edit profile.......", driver.current_url)

        #=======================Adding the website URL===============================

        # Wait for the website input field to be present
        wait = WebDriverWait(driver, 10)
        website_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-event='profile.edit.websiteUri']")))

        # Change the 'contenteditable' attribute to 'true'
        time.sleep(3)
        driver.execute_script("arguments[0].setAttribute('contenteditable', 'true')", website_input)

        # Click on the website input field to activate it
        ActionChains(driver).move_to_element(website_input).click().perform()
        time.sleep(3)

        # Input the desired website URL
        website_input.send_keys("https://www.example.com")
        time.sleep(2)
        # Optionally, you might need to confirm the input by pressing Enter or clicking a Save button
        website_input.send_keys(Keys.ENTER)

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)


if __name__ == "__main__":
    trial_users = [{"user_email":"user71342@additivedecor.com", "username":"gauravv98894","password":"Gaurav@3908799","zip_code":"10001","fullname":"Gaurav Thakur"},
                   {"user_email":"user56117@additivedecor.com", "username":"thakur5624443","password":"Thakur@352524","zip_code":"10002","fullname":"Gaurav T"}]    
    
    # user for sir
    # trial_users = [{"user_email":"vaibhavsir@additivedecor.com", "username":"vaibhav1141r","password":"Gaurav@321123"}, {"user_email":"user123@additivedecor.com", "username":"vaibhav1234sharda","password":"Gaurav@321123"}]
    for trail_creds in trial_users:
            
        main_email = 'gauravthakur81711296@gmail.com'
        app_pass = 'kbdu zqqn fkwl nflv'

        user_email = trail_creds["user_email"]
        username = trail_creds["username"]
        password = trail_creds["password"]
        fullname= trail_creds["fullname"]
        zip_code=trail_creds["zip_code"]

        site_url ="https://myspace.com/"
        signup_url="https://myspace.com/signup"
        login_url="https://myspace.com/signin"
        profile_edit_url= "https://myspace.com/settings/profile/edit"

        driver=create_driver()

        response = myspace_automation(password=password ,username=username,fullname=fullname,zip_code=zip_code,signup_url=signup_url,login_url=login_url,profile_edit_url=profile_edit_url,user_email=user_email,site_url=site_url)
        print(response)







