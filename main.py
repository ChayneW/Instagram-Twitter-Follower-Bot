from bs4 import BeautifulSoup
import requests
import csv
import re
import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


instagram_top_100 = 'https://www.socialtracker.io/toplists/top-100-instagram-users-by-followers/'
twitter_top_100 = 'https://www.socialtracker.io/toplists/top-100-twitter-users-by-followers/'


INSTAGRAM_URL = 'https://www.instagram.com/'
USERNAME = "Your username"
PASSWORD = "your password"


TWITTER_URL = 'https://twitter.com/'
TWITTER_EMAIL = 'your email'
TWITTER_USER = 'your username'
TWITTER_PASSWORD = 'your password'


s = Service('your chromedriver file path') #EX: /Users/chaynewhite/Development/chromedriver

influencers = []


'''Instagram Class to interact with, search pages, and follow.'''
class InstaFollower():

    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=driver_path)
        self.driver.get(INSTAGRAM_URL)
        time.sleep(5)

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)

        user_login = self.driver.find_element(By.NAME, 'username')
        time.sleep(3)
        user_password = self.driver.find_element(By.NAME, 'password')

        #user_login.click()
        user_login.send_keys(USERNAME)
        time.sleep(4)
        user_password.send_keys(PASSWORD)

        time.sleep(3)
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(10)


    def find_followers(self, account):

        self.driver.get(f'https://www.instagram.com/{account}')
        time.sleep(10)

        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/button/div/div').click()
        time.sleep(5)


'''Twitter Class to interact, search and follow twitter pages.'''
class TwitterFollower():

    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=driver_path)
        self.driver.get(TWITTER_URL)
        time.sleep(5)

    def login(self):
        time.sleep(10)

        self.driver.get('https://twitter.com/login')
        time.sleep(10)

        #email login
        print('tapping into the login website and finding login form')
        login_twitter = self.driver.find_element(By.TAG_NAME,'input')
        login_twitter.send_keys(TWITTER_EMAIL)

        # finding next button:
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div').click()

        time.sleep(5)
        print('tapping into finding input')

        # find txt box for acct check
        user_twitter = self.driver.find_element(By.NAME, 'text')
        user_twitter.send_keys(TWITTER_USER)
        time.sleep(4)

        next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "span")
        print('found next button?')

        time.sleep(2)

        # Span Items check to find next button:
        print(len(next_buttons)) #8

        test_text = "There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you."

        buttons_text = [s.text for s in next_buttons]
        print(buttons_text)

        # Username check if account has had unsucessful logins
        if test_text in buttons_text:
            print(f'Intermediate check triggered, True')
            next_buttons[-1].click()
            time.sleep(12)
        else:
            print(f'Intermediate check not triggered, check webpages.')
            pass

        #Password:
        password_twitter = self.driver.find_element(By.NAME, "password")
        password_twitter.send_keys(TWITTER_PASSWORD)
        time.sleep(2)

        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]').click()
        time.sleep(5)


    def find_followers(self, account):

        # Searching url
        self.driver.get(f"https://www.twitter.com/{f'{account}'}")
        time.sleep(5)

        # Searching 'Follow' button:
        self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/span/span').click()
        time.sleep(10)


#####################

'''Socialtracker.io website to web scrape top 100 accounts in Instagram:
    - Creates txt and csv files of web data scraped.'''
def top_100_scrape(social: str):

    if social == 'instagram':
        social_media_url = instagram_top_100

    elif social == 'twitter':
        social_media_url = twitter_top_100

    print('Please wait a moment. Processing...')
    response = requests.get(url=social_media_url)
    response.raise_for_status()
    social_page = response.text

    soup = BeautifulSoup(social_page, 'html.parser')

    for link in soup.find_all('a', class_='uk-link-reset uk-button-text'):
        user_name = link.get('href')
        print(user_name)
        user_name = user_name.replace(f'/{social}/','')#.strip('/instagram/')
        user_name = user_name.replace('/','')
        print(user_name)
        if len(user_name) < 1:
            pass
        
        else:
            influencers.append(user_name)
            with open(f'{social}_top_influencers.txt', mode='a') as f:
                f.write(f'{user_name}')
                f.write('\n')
                f.close()
    
    # Pandas file creation:
    followers_df = pandas.DataFrame(influencers, columns=['Name'])
    followers_df.to_csv(f'./{social}_top_influencers.csv', index=False)


'''use_files funct. uses files from previous funct. or add own files in same file directory.
    - Adjust file name and any spacing preferences in funct.
    - If not needed, comment funct. out. '''

def use_files(social: str):
    choice = str(input(f'txt or csv for {social}(only these 2 choices.) ')).lower()
    print(choice)

    if choice == 'txt':
    # TXT Extraction
    # Change txt file name to file desired.
        with open(f'{social}_top_influencers.txt', mode='r') as file:
            txt_list = file.readlines()
            influencers = [item.strip(',\n') for item in txt_list]
            print(f'returning list from txt') #\n{influencers}
            return influencers

    elif choice == 'csv':
    # CSV Extraction:
    # Change csv file name to file desired.
        with open(f'{social}_top_influencers.csv', mode='r') as file:
            csv_list = file.readlines()
            # print(csv_list)
            influencers = [item.strip(',\n') for item in csv_list]
            # removing the header (name)
            influencers.remove(influencers[0])
            print(f'returning list from csv')#\n{influencers}
            return influencers
    
    else:
        pass
    

'''Main Code starts here:'''
choice = str(input('What Social Media do you want to use for today?("instagram" or "twitter") ')).lower()
print(choice)

use_scraper = str(input(f'Do you want to use top 100 scraper for {choice}?("y" or "n") ')).lower()
if use_scraper == 'y':
    top_100_scrape(choice)
else:
    pass

print('\n')

files_ready = str(input(f'Do you have files(txt or csv) for the social followers for {choice} to to be used for searching?\nIf used web scraper, no need to answer "y".("y" or "n") ')).lower()
if files_ready == 'y':
    influencers = use_files(choice)
else:
    pass

print('will now start the automation.')

if choice == 'twitter':
    bot = TwitterFollower(s)

elif choice == 'instagram':
    bot = InstaFollower(s)

bot.login()

print(f'after use_files funct.\n{influencers}')
for user in influencers:
    print(user)
    time.sleep(5)
    bot.find_followers(user)
    time.sleep(4)
