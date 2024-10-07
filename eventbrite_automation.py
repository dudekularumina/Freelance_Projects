from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from email.parser import BytesParser
from email import policy
from bs4 import BeautifulSoup
import imaplib
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pyautogui



def create_driver():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def eventbrite_automation(password ,signup_url,eventcreate_url,firstname,lastname,user_email, site_url):
    try:
        # Open the website
        driver.get(site_url)
        time.sleep(10)

                
        # Add an explicit wait for the shadow DOM host element to be present
        # wait = WebDriverWait(driver, 20)
        # shadow_host = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#transcend-consent-manager")))

        pyautogui.press('enter')

      

        time.sleep(5)
        # ===================== Proceed to the signup page============================


        driver.get(signup_url)
        time.sleep(15)


        # time.sleep(10)


        
        email_login = driver.find_element(By.NAME,'email')
        email_login.send_keys(user_email)
        time.sleep(5)

        continue_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div/form/div[2]/div/button')
        continue_btn.click()
        time.sleep(10)

        confm_email=driver.find_element(By.ID,'emailConfirmation')
        confm_email.send_keys(user_email)
        time.sleep(5)

        first_name = driver.find_element(By.ID, "firstName")
        first_name.send_keys(firstname)
        time.sleep(5)
        
        lastname_input = driver.find_element(By.ID, "lastName")
        lastname_input.send_keys(lastname)
        time.sleep(5)

    
        password_input=driver.find_element(By.ID,'password')
        password_input.send_keys(password)
        time.sleep(5)

            # Example if checkbox has an id or a name:
            # Now, locate and click the checkbox using the 'for' attribute of the label
        checkbox = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='termsAccepted']"))
        )
        checkbox.click()
        time.sleep(8)

        create_acc=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div/form/div[3]/div/button')
        create_acc.click()
        time.sleep(20)


        # start_free_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/section/div/section/div/div[1]/section/div[2]/a/button')
        # start_free_btn.click() #                      //*[@id="root"]/div/div[2]/div/div[3]/div[2]/div[3]/button
        # time.sleep(5)

        
        # driver.get(home_url)    #updated
        # time.sleep(10)

        driver.get(eventcreate_url)
        time.sleep(15)

        btn=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[1]/div[1]/div[2]/div/div/button[4]')
        btn.click()
        time.sleep(5)

            # Select number of events
        events_select = Select(driver.find_element(By.ID, 'sales-select-field'))
        events_select.select_by_visible_text('2-5 events')
        time.sleep(5)


        # Select number of people
        people_select = Select(driver.find_element(By.ID, 'visitors-select-field'))
        people_select.select_by_visible_text('Up to 250 people')
        time.sleep(5)

            # Click on the <p> element with the specific text
        paragraph = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//p[@data-testid='subheading' and contains(text(), 'Something budget-friendly and easy to use')]"))
        )
        paragraph.click()
        time.sleep(5)    

        continue_btn1=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[1]/div[3]/div/a/button')
        continue_btn1.click()
        time.sleep(10)

        #+++++++++++++++login=+++++++++++++

        # driver.get('https://www.eventbrite.com/signin/?referrer=%2F')
        # time.sleep(8)

        # email_input=driver.find_element(By.ID,'email')
        # email_input.send_keys(main_email)
        # time.sleep(5)
        
        # password_input=driver.find_element(By.ID,'password')
        # password_input.send_keys(password)
        # time.sleep(5)

        # login_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div/div[2]/div/form/div[4]/div/button')
        # login_btn.click()
        # time.sleep(10)
        # #=========================================================




        driver.get(eventcreate_url)   #updated
        time.sleep(10)

        click_event=driver.find_element(By.XPATH,'//*[@id="EventOverviewPreview"]/h1')
        driver.execute_script("arguments[0].scrollIntoView(true);",click_event)
        click_event.click()
        time.sleep(5)
        
        event_title=driver.find_element(By.ID,'details-form-event-title')
        event_title.send_keys("Affiliate Marketing strategies and sales")
        time.sleep(5)

        event_sumamry=driver.find_element(By.ID,'details-form-summary')
        event_sumamry.send_keys("This event is about the Affiliate Marketing Conference and Sales strategies")
        time.sleep(5)

        venue_loc=driver.find_element(By.XPATH,'//*[@id="DateAndVenuePreview"]/div/div[1]/div[3]/div/h1')
        driver.execute_script("arguments[0].scrollIntoView(true);",venue_loc)
        venue_loc.click()
        time.sleep(10)

        venue_loc_input=driver.find_element(By.ID,'VenueLocationField')
        driver.execute_script("arguments[0].scrollIntoView(true);",venue_loc_input)
        venue_loc_input.send_keys("Hyderabad")
            # Press the "Enter" key after entering the location
        # venue_loc_input.send_keys(Keys.RETURN)  # or use Keys.ENTER

        # Optional: Wait a bit to ensure the page or element updates after pressing "Enter"
        time.sleep(10)

        # venue_add1=driver.find_element(By.ID,'event-simplification-form-venue-address1')
        # venue_add1.send_keys("Hyderabad")
        # time.sleep(5)

        # venue_zip=driver.find_element(By.ID,'event-simplification-form-venue-zipcode')
        # venue_zip.send_keys("500016")
        # time.sleep(5)

        save_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[1]/div/main/section/div/form/footer/div/button')
        save_btn.click()
        time.sleep(20)

        free_tickets_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[1]/div/main/section/div/div/div/div[2]/div[2]/div/div[2]/button')
        free_tickets_btn.click()
        time.sleep(5)

        ticket_quantity=driver.find_element(By.ID,'ticket-quantity')
        ticket_quantity.send_keys("88")
        time.sleep(7)

        save_btn1=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/section/div[2]/div/div/div[2]/div/div[2]/button')
        save_btn1.click()
        time.sleep(20)

        next_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/button')
        next_btn.click()                      #//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/button
        time.sleep(15)

        publish_btn=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/section/div/div/div/form/footer/div/button')
        publish_btn.click()                      #//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/section/div/div/div/form/footer/div/button
        time.sleep(10)

        print("Current URL",driver.current_url)
        time.sleep(10)
        print()
        print("**"*60)
        print()

        return  {"status": "success", "message": "Profile updated successfully!", "payload":f"return url: {driver.current_url}"}
        
    except Exception as e:
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        time.sleep(10)
    


if __name__ == "__main__":
    trial_users = [{"user_email":"user236@additivedecor.com", "username":"gauravr665364","password":"Gaurav@37673738"}, {"user_email":"user5467@additivedecor.com", "username":"Thakur564747434","password":"Gaurav@367575623"}]    
    
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

        signup_url="https://www.eventbrite.ie/signin/signup/?referrer=%2F"
        
        eventcreate_url='https://www.eventbrite.ie/manage/events/create' #https://www.eventbrite.com/manage/events/auto-create
        site_url = 'https://www.eventbrite.ie/'

         # Create a new browser instance for each iteration
        driver = create_driver()

        response = eventbrite_automation( password=password, signup_url=signup_url,eventcreate_url=eventcreate_url, firstname=firstname, lastname=lastname,user_email=user_email, site_url=site_url)
        print(response)

        time.sleep(10) 
    












    
