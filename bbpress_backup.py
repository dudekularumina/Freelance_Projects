from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import imaplib
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
import re

# Anti-Captcha API key
API_KEY = '8a49a20ff3faacb672dcee697adec6f0'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

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
        print("task finished with error " + solver.error_code)
        return None

def extract_link_from_text(text):
    # Regular expression to find URLs in the text
    url_pattern = re.compile(r'(https?://[^\s]+)')
    urls = url_pattern.findall(text)
    for url in urls:
        if "wordpress.org" in url:
            return url
    return None

def get_confirmation_link(email_id, app_password):
    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email_id, app_password)
        imap.select('inbox')
        time.sleep(3)

        # Search for all emails in the inbox
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        time.sleep(2)

        # Fetch the latest 10 emails
        latest_email_ids = list(reversed(email_ids[-10:]))

        for email_id in latest_email_ids:
            _, msg_data = imap.fetch(email_id, '(RFC822)')
            time.sleep(2)
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])

            # Initialize email content
            email_content = None

            # Check if the email is multipart
            if msg.is_multipart():
                for part in msg.iter_parts():
                    if part.get_content_type() == 'text/html':
                        html_content = part.get_payload(decode=True)
                        soup = BeautifulSoup(html_content, 'html.parser')
                        email_content = soup.get_text()
                        print("HTML part found. Content:")
                        print(email_content)  # Log the HTML content
                        # Check for "WordPress" in the HTML content
                        if "WordPress" in email_content:
                            link = soup.find('a', href=True)
                            if link:
                                print("Confirmation link found in HTML part.")
                                return link['href']
                    elif part.get_content_type() == 'text/plain':
                        email_content = part.get_payload(decode=True).decode()
                        print("Plain text part found. Content:")
                        print(email_content)  # Log the plain text content
                        # Check for "WordPress" in the plain text content
                        if "WordPress" in email_content:
                            link = extract_link_from_text(email_content)
                            if link:
                                print("Confirmation link found in plain text part.")
                                return link
            else:
                if msg.get_content_type() == 'text/html':
                    html_content = msg.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    email_content = soup.get_text()
                    print("HTML email found. Content:")
                    print(email_content)  # Log the HTML content
                    # Check for "WordPress" in the HTML content
                    if "WordPress" in email_content:
                        link = soup.find('a', href=True)
                        if link:
                            print("Confirmation link found in HTML email.")
                            return link['href']
                elif msg.get_content_type() == 'text/plain':
                    email_content = msg.get_payload(decode=True).decode()
                    print("Plain text email found. Content:")
                    print(email_content)  # Log the plain text content
                    # Check for "WordPress" in the plain text content
                    if "WordPress" in email_content:
                        link = extract_link_from_text(email_content)
                        if link:
                            print("Confirmation link found in plain text email.")
                            return link

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        imap.logout()

try:
    driver.get("https://login.wordpress.org/register?locale=en_US")

    username_input = driver.find_element(By.ID, "user_login")
    time.sleep(2)
    username_input.send_keys("dudekula" + "rumina122")

    email_input = driver.find_element(By.ID, "user_email")
    time.sleep(2)
    email_input.send_keys("d.rumina4122" + "@gmail.com")
    time.sleep(3)

    terms_checkbox = driver.find_element(By.ID, "terms_of_service")
    if not terms_checkbox.is_selected():
        terms_checkbox.click()
    time.sleep(3)

    mailing_list_checkbox = driver.find_element(By.ID, "user_mailinglist")
    if not mailing_list_checkbox.is_selected():
        mailing_list_checkbox.click()
    time.sleep(3)

    site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
    current_url = driver.current_url
    recaptcha_response = solve_recaptcha(site_key, current_url)

    if recaptcha_response:
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
        time.sleep(2)
        create_account_button = driver.find_element(By.ID, "wp-submit")
        time.sleep(3)
        create_account_button.click()

    time.sleep(10)

    email_id = "d.rumina4122@gmail.com"
    app_password = "akau ftel sutp yjxl"

    confirmation_link = get_confirmation_link(email_id, app_password)
    if confirmation_link:
        driver.get(confirmation_link)
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass1")))

        password_input = driver.find_element(By.ID, "pass1")
        time.sleep(2)
        password_input.clear()
        time.sleep(2)
        password_input.send_keys("Rumina@41228")

        website_input = driver.find_element(By.ID, "user_url")
        time.sleep(2)
        website_input.send_keys("https://mysiteus.com")

        location_input = driver.find_element(By.ID, "user_location")
        time.sleep(2)
        location_input.send_keys("New York")

        occupation_input = driver.find_element(By.ID, "user_occupation")
        time.sleep(2)
        occupation_input.send_keys("Developer")

        interests_input = driver.find_element(By.ID, "user_interests")
        time.sleep(2)
        interests_input.send_keys("technology, innovation")

        site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        current_url = driver.current_url
        recaptcha_response = solve_recaptcha(site_key, current_url)

        if recaptcha_response:
            driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
            time.sleep(2)
            create_account_button = driver.find_element(By.ID, "wp-submit")
            time.sleep(2)
            create_account_button.click()

            time.sleep(10)

            driver.get("https://login.wordpress.org/?from=bbpress.org&redirect_to=https%3A%2F%2Fbbpress.org%2Fregister&locale=en_US")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login")))

            username_input = driver.find_element(By.ID, "user_login")
            time.sleep(2)
            username_input.send_keys("dudekularumina122")

            password_input = driver.find_element(By.ID, "user_pass")
            time.sleep(2)
            password_input.send_keys("Rumina@41228")

            site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            current_url = driver.current_url
            recaptcha_response = solve_recaptcha(site_key, current_url)

            if recaptcha_response:
                driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_response}";')
                time.sleep(2)
                login_button = driver.find_element(By.ID, "wp-submit")
                time.sleep(2)
                login_button.click()

                WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
                current_url = driver.current_url
                print(f"Current URL after login: {current_url}")

    else:
        print("No confirmation link found.")

finally:
    driver.quit()

# ==========================================================================================================


