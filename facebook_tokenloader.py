"""Retrieves a Tinder XAuthToken for a registered user"""
import time
import re

from getpass import getpass

from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


def display_warning():
    """Displays warning other info"""
    print("Get Tinder Access Token - Retrieves a Tinder XAuthToken")
    print("Author: Kotaro Yama (kotaro.h.yama@gmail.com)")
    print("\nNOTE: You need to have registered on Tinder app or website with your Facebook account first\n")
    print("\nAlso, you do not have to do anything while the browser is doing its job.")

def parse_auth(html_doc):
    """Parses the access_token out of the html page"""
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Find the script tag that has window.location.href
    #   There seem to be two <script> tags in the html
    #   The one that contains the acccess_token has a type attribute, and the
    #   other one doesn't.
    script_content = soup.find(type="text/javascript").string

    # Extract the regular expression match of the access_token and get the match string
    access_token_string = re.search('access_token=[a-zA-Z0-9]*&', script_content).group(0)

    # Polish the regular string again
    access_token_string_modified = re.search('[a-zA-Z0-9]*&', access_token_string).group(0)
    access_token_string_final = re.search('[a-zA-Z0-9]*', access_token_string_modified).group(0)

    return access_token_string_final

def get_xauth_token(long_token):
    """Retrieves the XAuthToken using the access_token_string"""
    USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"

    HEADERS = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "content-type": "application/json",
        "User-agent": USER_AGENT,
        "Accept": "application/json"
    }

    
    new_url = 'https://www.facebook.com/login.php?skip_api_login=1&api_key=464891386855067&kid_directed_site=0&app_id=464891386855067&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.8%2Fdialog%2Foauth%3Fapp_id%3D464891386855067%26cbt%3D1692460759524%26channel_url%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fx%252Fconnect%252Fxd_arbiter%252F%253Fversion%253D46%2523cb%253Df126b014142bacc%2526domain%253Dtinder.com%2526is_canvas%253Dfalse%2526origin%253Dhttps%25253A%25252F%25252Ftinder.com%25252Ff24bf898f0bad%2526relation%253Dopener%26client_id%3D464891386855067%26display%3Dpopup%26domain%3Dtinder.com%26e2e%3D%257B%257D%26fallback_redirect_uri%3Dhttps%253A%252F%252Ftinder.com%252F%26locale%3Den_US%26logger_id%3Df28655b03bf57a8%26origin%3D1%26redirect_uri%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fx%252Fconnect%252Fxd_arbiter%252F%253Fversion%253D46%2523cb%253Df22ab7e73ba31bc%2526domain%253Dtinder.com%2526is_canvas%253Dfalse%2526origin%253Dhttps%25253A%25252F%25252Ftinder.com%25252Ff24bf898f0bad%2526relation%253Dopener%2526frame%253Df1aa9d41857d6c4%26response_type%3Dtoken%252Csigned_request%252Cgraph_domain%26scope%3Duser_birthday%252Cuser_photos%252Cemail%252Cuser_likes%26sdk%3Djoey%26version%3Dv2.8%26ret%3Dlogin%26fbapp_pres%3D0%26tp%3Dunspecified&cancel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df22ab7e73ba31bc%26domain%3Dtinder.com%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252Ftinder.com%252Ff24bf898f0bad%26relation%3Dopener%26frame%3Df1aa9d41857d6c4%26error%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied&display=popup&locale=en_GB&pl_dbl=0'
    new_data = {"token": long_token}
    r_new = requests.post(new_url, headers=HEADERS, json=new_data)

    return r_new.json()

def main():
    display_warning()
    
    # Option to block the notification popup (for Google Chrome)
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    # Iterate the loop until the user enters correct email and password
    while True:
        try:
            # Login info (Facebook)
            email_adrs = input('Email: ')
            password = getpass() 

            # Automatically installs the chrome driver
            chromedriver_autoinstaller.install() 
            driver = webdriver.Chrome()
            driver.get("https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y")

            # Email input
            email_text = driver.find_element_by_id("email")
            email_text.send_keys(email_adrs)
            # Password input
            password_text = driver.find_element_by_id("pass")
            password_text.send_keys(password)

            # Submit
            password_text.submit()

            # Get the continue button
            time.sleep(3)
            continue_button = driver.find_element_by_css_selector('div[aria-label="Continue"]')

            break
        except Exception as e:
            driver.close()
            print('Incorrect credential, try again...\n')

    continue_button.click()

    # page_source property has the html source
    long_token = parse_auth(driver.page_source)

    # Close the driver for the long token
    driver.close()

    # Print out the XAuthToken
    xauth = get_xauth_token(long_token)['data']['api_token']
    print(f"\nXAuthToken: {xauth}")

if __name__ == '__main__':
    main()