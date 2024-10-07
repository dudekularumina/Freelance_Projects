from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random


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


def justpasteit_automation( site_url):
        
    try:
        driver.get(site_url)
        time.sleep(10)

        link_btn=driver.find_element(By.XPATH,'//*[@id="htmlAreaDIV"]/div/div[1]/div[1]/div[1]/div/div[3]/button[1]')
        link_btn.click()
        time.sleep(10)

        url_input=driver.find_element(By.CLASS_NAME,'tox-textfield')
        url_input.send_keys('https://www.sample.com')
        time.sleep(10)

        # text_input=driver.find_element(By.ID,'form-field_3864212502871725883928624')
        # text_input.clear()
        # text_input.send_keys('sample url')
        # time.sleep(10)

        save_btn=driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/button[2]')
        save_btn.click()
        time.sleep(10)

    # Enable and click the Publish button
        publish_btn = driver.find_element(By.CSS_SELECTOR, '.publishButton')

        # Execute JavaScript to remove 'disabled' attribute
        driver.execute_script("arguments[0].removeAttribute('disabled');", publish_btn)
        
        # Click the button after enabling it
        publish_btn.click()
        time.sleep(15)
        
       
        try:
            # captcha_images = driver.find_elements(By.CLASS_NAME, 'clickableImage')

            
            while True:
                # Start random clicks on CAPTCHA images
                captcha_images = driver.find_elements(By.CLASS_NAME, 'clickableImage')

                # Randomly click 3 or 4 images
                for _ in range(random.randint(4, 6)):
                    random_image = random.choice(captcha_images)
                    random_image.click()
                    time.sleep(3)  # Short delay between clicks

                # Click the "Verify" button
                verify_btn = driver.find_element(By.CSS_SELECTOR, '.CaptchaButtonVerify')
                verify_btn.click()
                time.sleep(10)

        #         # Check if the "Try New" button appears
        #         try_new_btn = driver.find_elements(By.XPATH, '//*[@id="editArticleWidget"]/div/div[1]/div/div[1]/div[3]/div/div/div[12]/button')
        #         if try_new_btn:
        #             try_new_btn[0].click()
        #             print("Clicked on 'Try New' button. CAPTCHA reset.")
        #             time.sleep(5)  # Allow time for the new CAPTCHA to load
        #         else:
        #             # Check if the "Publish" button is enabled
        #             publish_button = driver.find_element(By.CSS_SELECTOR, '.publishButton')
        #             if publish_button.is_enabled():
        #                 print("CAPTCHA solved and Publish button enabled.")
        #                 publish_button.click()  # Click the publish button
        #                 break
        #             else:
        #                 print("Publish button still disabled. Trying again...")
        #                 time.sleep(10)

                print("Current URL",driver.current_url)
                
            # Enable and click the Publish button
                publish_btn = driver.find_element(By.CSS_SELECTOR, '.publishButton')

                # Execute JavaScript to remove 'disabled' attribute
                driver.execute_script("arguments[0].removeAttribute('disabled');", publish_btn)
                
                # Click the button after enabling it
                publish_btn.click()
                time.sleep(25)
        except:
            print("Except executed")
    

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}


    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":

    for _ in range(2):
        site_url = 'https://justpaste.it/'
        
        driver=create_driver()

        response = justpasteit_automation(site_url)
        print(response)