from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Open in incognito mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
def flickr_automation(email_id, email_password,  site_url):
    try:
        # Open the website
        driver.get(site_url)
        print("Website loaded")
        time.sleep(2)  # Wait for 2 seconds

        # Click on the Signup button using link text
        signup_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))
        )
        signup_button.click()
        print("Sign Up button clicked")
        time.sleep(2)  # Wait for 2 seconds

        # Wait for the signup page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "sign-up-first-name"))
        )
        print("Signup page loaded")
        time.sleep(2)  # Wait for 2 seconds

        # Fill in the form
        driver.find_element(By.ID, "sign-up-first-name").send_keys("D.")
        time.sleep(1)
        driver.find_element(By.ID, "sign-up-last-name").send_keys("Rumina")
        time.sleep(1)
        driver.find_element(By.ID, "sign-up-age").send_keys("23")
        time.sleep(1)
        driver.find_element(By.ID, "sign-up-email").send_keys(email_id)
        time.sleep(1)
        driver.find_element(By.ID, "sign-up-password").send_keys("ruminadudekula888")
        print("Form filled")
        time.sleep(2)  # Wait for 2 seconds

        # Handle reCAPTCHA
        try:
            iframe = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='recaptcha']"))
            )
            driver.switch_to.frame(iframe)
            print("Switched to reCAPTCHA iframe")
            time.sleep(2)  # Wait for 2 seconds

            recaptcha_checkbox = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )
            recaptcha_checkbox.click()
            print("reCAPTCHA checkbox clicked")
            time.sleep(2)  # Wait for 2 seconds

            driver.switch_to.default_content()
            print("Switched back to default content")
            time.sleep(2)  # Wait for 2 seconds

            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element((By.ID, "recaptcha-anchor"))
            )
            print("reCAPTCHA completed")
            time.sleep(2)  # Wait for 2 seconds

        except Exception as e:
            print(f"CAPTCHA handling failed: {e}")

        # Scroll the Signup button into view and click using JavaScript
        signup_button_final = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='identity-form-submit-button']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", signup_button_final)
        time.sleep(1)  # Wait for 1 second

        driver.execute_script("arguments[0].click();", signup_button_final)
        print("Signup button clicked")
        time.sleep(5) 

        # Check if the page has redirected or opened a new window
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        time.sleep(5)  # Wait to see if there's any redirection or response
    

        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url ="https://www.flickr.com"

    response = flickr_automation(email_id, email_password,  site_url)
    print(response)
