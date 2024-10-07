from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
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
def imgur_automation(email_id,email_password,site_url):
    try:
        # Open Imgur registration page
        driver.get(site_url)
        time.sleep(5)

        # Wait until the Sign Up button is clickable and click it
        sign_up_button = driver.find_element(By.CLASS_NAME, "ButtonLink")
        sign_up_button.click()

        # Fill in the form fields with a delay
        time.sleep(3)
        driver.find_element(By.ID, "username").send_keys("ruminadudekula")
        time.sleep(3)
        driver.find_element(By.ID, "email").send_keys(email_id)
        time.sleep(3)
        driver.find_element(By.ID, "password").send_keys("hjg54@41228")
        time.sleep(3)
        driver.find_element(By.ID, "confirm_password").send_keys("hjg54@41228")
        time.sleep(3)
        driver.find_element(By.ID, "phone_number").send_keys("")

        # Click on the Next button
        time.sleep(3)
        next_button = driver.find_element(By.ID, "Imgur")
        next_button.click()

        # Wait for the reCAPTCHA to appear and solve it
        time.sleep(10)  # Give time for the page to load the reCAPTCHA
        site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        url = driver.current_url
        recaptcha_response = solve_recaptcha(site_key, url)

        if recaptcha_response:
            # Fill in the reCAPTCHA response
            driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(recaptcha_response))

            # Submit the form (if there's a submit button, click it; otherwise, use a different method)
            time.sleep(3)
            submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-action')]")
            submit_button.click()

            # Wait for a while to observe the result
            time.sleep(10)
        else:
            print("Failed to solve reCAPTCHA")
        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url = "https://imgur.com/"

    response = imgur_automation(email_id, email_password,  site_url)
    print(response)
