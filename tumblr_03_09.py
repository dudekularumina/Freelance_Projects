from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'


# Initialize Anti-Captcha client
solver = hCaptchaProxyless()
solver.set_key(API_KEY)


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

def tumblr_automation(main_email,app_pass,user_email,blog_url,site_url):

    try:
        driver.get(site_url)
        time.sleep(10)

        signup=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div/div[2]/div[1]/div/div[2]/button[1]')
        signup.click()
        time.sleep(10)

        email_input_btn=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/button')
        email_input_btn.click()
        time.sleep(5)

        email_input=driver.find_element(By.NAME,'email')
        email_input.send_keys(user_email)
        time.sleep(5)

        next_btn=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/div[1]/button')
        next_btn.click()
        time.sleep(5)
        
        pasword_input=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/div/div[1]/input')
        pasword_input.send_keys(password)
        time.sleep(5)

        pasword_input_cnfm=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/div/input')
        pasword_input_cnfm.send_keys(password)
        time.sleep(10)

        next_btn1=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/div/div[2]/button')
        next_btn1.click()
        time.sleep(5)

        # Assuming you want to interact with a dropdown element with name 'month'
        select_element = driver.find_element(By.NAME, 'month')
        select = Select(select_element)
        select.select_by_visible_text('May')
        time.sleep(5)

        # Assuming you want to interact with a dropdown element with name 'month'
        select_element = driver.find_element(By.NAME, 'day')
        select = Select(select_element)
        select.select_by_visible_text('5')
        time.sleep(5)


        # Assuming you want to interact with a dropdown element with name 'month'
        select_element = driver.find_element(By.NAME, 'year')
        select = Select(select_element)
        select.select_by_visible_text('1999')
        time.sleep(5)

        
        next_btn2=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/form/div[1]/div[2]/button')
        next_btn2.click()
        time.sleep(5)
        
        blog_name=driver.find_element(By.ID,'onboardingBlogname')
        blog_name.send_keys(blogname)
        time.sleep(8)

        signup_btn=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div[1]/div/div/div/div/div/form/div[2]/button')
        signup_btn.click()
        time.sleep(30)

        #===========Follow Topics===============

        click1=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[2]/section[4]/div/div/button[1]')
        click1.click()
        time.sleep(5)

        next_btn3=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[1]/div[2]/div[2]/div/button')
        next_btn3.click()
        time.sleep(10)

        follow_btn1=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[2]/div/section[1]/div[2]/div/div[2]/div/div[2]/div[1]/button')
        follow_btn1.click()
        time.sleep(5)

        follow_btn2=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[2]/div/section[1]/div[2]/div/div[3]/div/div[2]/div[1]/button')
        follow_btn2.click()
        time.sleep(5)

        follow_btn3=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[2]/div/section[1]/div[2]/div/div[5]/div/div[2]/div[1]/button')
        follow_btn3.click()
        time.sleep(5)

        
        next_btn4=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div[1]/div[2]/div[2]/div/button')
        next_btn4.click()
        time.sleep(15)

        print('Current URL==',driver.current_url)
        time.sleep(5)

        create_post=driver.find_element(By.XPATH,'//*[@id="base-container"]/div[2]/div/div[1]/div/div[2]/div[2]/a')
        create_post.click()
        time.sleep(5)

        link_btn=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div[4]/div/a')
        link_btn.click()
        time.sleep(5)

        link_input=driver.find_element(By.XPATH,'//*[@id="block-10e862bc-dbfc-437c-b566-b852f8b061b8"]/div/div/div/input')
        link_input.send_keys('https://sample.com')
        time.sleep(5)

        insert_btn=driver.find_element(By.XPATH,'//*[@id="block-10e862bc-dbfc-437c-b566-b852f8b061b8"]/div/div[2]/button')
        insert_btn.click()
        time.sleep(8)

        add_tags=driver.find_element(By.CLASS_NAME,'mbROR')
        add_tags.click()
        time.sleep(3)
        add_tags.send_keys("#animals")
        time.sleep(5)

        post_now_btn=driver.find_element(By.XPATH,'//*[@id="glass-container"]/div/div/div/div/div/div/div[2]/div/div[3]/div/div/div/button')
        post_now_btn.click()
        time.sleep(10)

        driver.get(blog_url)

        time.sleep(10)
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

    password='Gaurav@4122'
    blogname='gauravth8116'

    site_url = 'https://www.tumblr.com/'
    blog_url=f'https://www.tumblr.com/blog/{blogname}'

    response = tumblr_automation(main_email, app_pass,user_email,blog_url, site_url)
    print(response)
    time.sleep(10)