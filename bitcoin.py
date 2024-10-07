from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import ElementClickInterceptedException
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import imaplib
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.alert import Alert
import requests
import speech_recognition as sr
import os
import pytesseract
from PIL import Image
import requests
from io import BytesIO


# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'



# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

#================audio Captcha========================

# # Function to download the audio CAPTCHA
# def download_audio(url):
#     audio_file = 'captcha_audio.mp3'
#     response = requests.get(url)
#     with open(audio_file, 'wb') as file:
#         file.write(response.content)
#     return audio_file

# # Function to convert the audio CAPTCHA to text
# def convert_audio_to_text(audio_file):
#     recognizer = sr.Recognizer()
#     time.sleep(2)

#     with sr.AudioFile(audio_file) as source:
#         audio = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         return text
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#         return None
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
#         return None

#=======================================================

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

def bitcoin_automation(email_id, email_password,  site_url):

    try:
        driver.get(site_url)
        time.sleep(10)

        driver.get('https://bitcointalk.org/index.php?action=register')
        time.sleep(6)

        username=driver.find_element(By.NAME,'user')
        username.send_keys('gauravthakur')
        time.sleep(5)

        email_input=driver.find_element(By.NAME,'email')
        email_input.send_keys(email_id)
        time.sleep(5)
        
        passwrd1_input=driver.find_element(By.NAME,'passwrd1')
        passwrd1_input.send_keys('Gaurav@4122')
        time.sleep(5)

        passwrd2_input=driver.find_element(By.NAME,'passwrd2')
        passwrd2_input.send_keys('Gaurav@4122')
        time.sleep(5)

    #============================================================
        
        # # Download and process the audio CAPTCHA
        # audio_url = driver.find_element(By.XPATH, '//*[@id="creator"]/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]/div/a[1]').get_attribute('href')
        # audio_file = download_audio(audio_url)
        # time.sleep(3)
        # verification_code = convert_audio_to_text(audio_file)
        # time.sleep(3)


        # # Clean up downloaded audio file
        # os.remove(audio_file)
        # time.sleep(3)

        # # Enter the verification code
        # visual_code = driver.find_element(By.NAME, 'visual_verification_code')
        # visual_code.send_keys(verification_code)
        # time.sleep(10)

    #============================================================
            
        # Specify the path to tesseract executable if needed
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


        # Ensure the CAPTCHA is fully visible before taking the screenshot
        captcha_element = driver.find_element(By.ID, 'verificiation_image')
        driver.execute_script("arguments[0].scrollIntoView();", captcha_element)

        # Capture a screenshot of the entire page
        driver.save_screenshot('full_screenshot.png')

        # Locate the CAPTCHA image element
        location = captcha_element.location
        size = captcha_element.size

        # Calculate the bounding box (left, upper, right, lower) to crop the CAPTCHA image
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        # Ensure the calculated bounding box is within the image boundaries
        full_image = Image.open('full_screenshot.png')
        img_width, img_height = full_image.size

        # Adjust the bounding box if it extends beyond the image
        right = min(right, img_width)
        bottom = min(bottom, img_height)

        # Crop the CAPTCHA image from the screenshot
        captcha_image = full_image.crop((left, top, right, bottom))

        # Save the cropped image for verification (optional)
        captcha_image.save('captcha_image.png')

        # Use OCR to extract text from the CAPTCHA image
        captcha_text = pytesseract.image_to_string(captcha_image).strip()

        # Enter the CAPTCHA text into the verification field
        visual_code = driver.find_element(By.NAME, 'visual_verification_code')
        visual_code.send_keys(captcha_text)

        # Optionally, print or log the recognized text
        print("Recognized CAPTCHA text:", captcha_text)

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

        submit_btn=driver.find_element(By.XPATH,'//*[@id="creator"]/div/input')
        submit_btn.click()
        time.sleep(8)
        return{"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    email_id =   'hi@additivedecor.com' 'gauravthakur81711296@gmail.com'      
    email_password ='kbdu zqqn fkwl nflv'
    # about_content = "<a href='https://novusaurelius.com/'> My Site </a>"
    site_url = 'https://bitcointalk.org/'

    response = bitcoin_automation(email_id, email_password,  site_url)
    print(response)
