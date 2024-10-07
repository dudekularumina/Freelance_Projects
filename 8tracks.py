

#==============Not Working Giving This Msg"8tracks is only for the USA And Canada Users=======================


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Open in incognito mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def solve_recaptcha(site_key, url):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(url)
    solver.set_website_key(site_key)

    response = solver.solve_and_return_solution()
    if response != 0:
        return response
    else:
        print("Task finished with error: " + solver.error_code)
        return None

def eight_tracks_automation(main_email, app_pass,password ,username,user_email, display_name,  about_content, site_url):
    try:
        # Wait for the link to load and then click it
                
        # Open the website
        driver.get(site_url)

        wait = WebDriverWait(driver, 20)
        try:
            link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.flatbutton.button_gradient")))
            link.click()
            print("Link clicked")
        except Exception as e:
            print(f"Link clicking failed: {e}")

        # Print the current URL
        print("Current URL:", driver.current_url)

        # Fill out the email field
        email_input = wait.until(EC.presence_of_element_located((By.ID, "user_email")))
        email_input.send_keys(main_email)
        time.sleep(5)

        # Fill out the username field

        username_input = wait.until(EC.presence_of_element_located((By.ID, "user_login")))
        username_input.send_keys(username)
        time.sleep(5)

        # Fill out the password field
        password_input = wait.until(EC.presence_of_element_located((By.ID, "user_password")))
        password_input.send_keys(password)
        time.sleep(5)

        # Handle reCAPTCHA
        try:
            iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']")))
            driver.switch_to.frame(iframe)
            print("Switched to reCAPTCHA iframe")
            time.sleep(5)

            recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
            recaptcha_checkbox.click()
            print("reCAPTCHA checkbox clicked")
            time.sleep(5)

            driver.switch_to.default_content()
            print("Switched back to default content")

            # Solve reCAPTCHA
            site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            current_url = driver.current_url
            recaptcha_response = solve_recaptcha(site_key, current_url)

            if recaptcha_response:
                driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
                print("reCAPTCHA solved")
                time.sleep(5)
            else:
                print("Failed to solve reCAPTCHA")
                

        except Exception as e:
            print(f"CAPTCHA handling failed: {e}")

        # Click the "Sign up" button using JavaScript
        signup_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit")))
        driver.execute_script("arguments[0].click();", signup_button)
        print("Sign up button clicked")

        # Wait to see the result of the click
        time.sleep(20)
        print("Current URL:", driver.current_url)
        driver.back()
    

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
    site_url='https://8tracks.com/'

    response=eight_tracks_automation(main_email, app_pass,password ,username,user_email, display_name,  about_content, site_url)
    print(response)
    time.sleep(10)


