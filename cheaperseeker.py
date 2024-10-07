


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from PIL import Image
import pytesseract
import requests
from io import BytesIO

# Path to the Tesseract executable (update this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def solve_captcha_image(captcha_url):
    try:
        # Download CAPTCHA image
        response = requests.get(captcha_url)
        response.raise_for_status()  # Raise an error if the request fails

        # Open image with PIL and use Tesseract to extract text
        image = Image.open(BytesIO(response.content))
        captcha_text = pytesseract.image_to_string(image).strip()
        return captcha_text
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")
        return ""
def cheaperseeker_automation(email_id, email_password,  site_url):
    try:
        driver.get(site_url)
        time.sleep(4)
        # Open the registration page
        driver.get("https://www.cheaperseeker.com/register")
        time.sleep(5)
        
        # Fill in registration details
        username = driver.find_element(By.NAME, "username")
        username.clear()
        username.send_keys("gauravthakur")
        time.sleep(2)

        email = driver.find_element(By.NAME, "email")
        email.send_keys("gauravthakur81711296@gmail.com")
        time.sleep(2)

        password = driver.find_element(By.NAME, "password")
        password.send_keys("Gaurav@81711296")
        time.sleep(2)

        confirm_password = driver.find_element(By.NAME, "confirm_password")
        confirm_password.send_keys("Gaurav@81711296")
        time.sleep(2)

        # Locate CAPTCHA image
        captcha_image = driver.find_element(By.CSS_SELECTOR, 'img.captcha')
        captcha_url = captcha_image.get_attribute('src')

        # Solve CAPTCHA
        captcha_text = solve_captcha_image(captcha_url)
        print(f"Captcha text: {captcha_text}")

        if captcha_text:
            # Enter CAPTCHA text
            captcha_input = driver.find_element(By.NAME, "captcha")  # Update with actual name if different
            captcha_input.send_keys(captcha_text)
            time.sleep(2)

            # Click the register button
            register_button = driver.find_element(By.CSS_SELECTOR, "#main > div > form > button")
            register_button.click()
            time.sleep(5)

            print("Registration button clicked.")
        else:
            print("Failed to solve CAPTCHA.")
        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =    'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url = "https://www.cheaperseeker.com"

    response = cheaperseeker_automation(email_id, email_password,  site_url)
    print(response)