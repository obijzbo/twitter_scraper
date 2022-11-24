import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from settings.config import URL, WAIT, MEDIUM_WAIT, LONG_WAIT, EMAIL, PASSWORD, USER, NUMBER_OF_POST
from functions import make_dir
import re

class TwitterScraper:
    def __init__(self, driver, data_path, info_path):
        self.wait = WAIT
        self.medium_wait = MEDIUM_WAIT
        self.long_wait = LONG_WAIT
        self.site_link = URL
        self.driver = driver
        self.data_path = data_path
        self.info_path = info_path
        self.email = EMAIL
        self.password = PASSWORD
        self.user = USER
        self.tweet_links = []
        self.px = int()
        self.run_scraper()
        pass

    def run_scraper(self):
        self.open_web_page()
        time.sleep(self.wait)
        self.login()
        time.sleep(self.wait)
        self.get_page()
        time.sleep(self.wait)
        if not os.path.isfile(f"{self.info_path}/link.json"):
            self.get_tweet_link()
        if not os.path.isfile(f"{self.info_path}/data.json"):
            self.get_tweet_data()
        pass

    def open_web_page(self):
        self.driver.get(self.site_link)

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def login(self):
        try:
            log_in = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@href="/login"]'))
            )
            log_in.click()
        except:
            print("Log in page not found!!!")

        try:
            email_box = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@autocomplete="username"]'))
            )
            email_box.clear()
            email_box.send_keys(self.email)
        except:
            print("Email not found!!!")

        try:
            next_btn = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[text()="Next"]'))
            )
            next_btn.click()
        except:
            print("Next button not found!!!")

        try:
            name_box = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@data-testid="ocfEnterTextTextInput"]'))
            )
            name_box.clear()
            name_box.send_keys(self.user)

            next_btn = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[text()="Next"]'))
            )
            next_btn.click()
        except:
            print("Authentication not needed!!!!")

        try:
            password_box = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@name="password"]'))
            )
            password_box.clear()
            password_box.send_keys(self.password)
        except:
            print("Password not found!!!")

        try:
            log_in_button = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]'))
            )
            log_in_button.click()
        except:
            print("Log in not found!!!")
        time.sleep(self.wait)
        pass

    def get_page(self):
        page = WebDriverWait(self.driver, self.medium_wait).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '//span[text()="@bbcbangla"]'))
                                )
        page.click()

    def save_to_json(self):
        with open(f"{self.info_path}/link.json", 'w') as file:
            json.dump(self.tweet_links, file, indent=4)

    def get_tweet_link(self):
        while len(self.tweet_links) < NUMBER_OF_POST:
            post_elements = WebDriverWait(self.driver, self.medium_wait).until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH, '//div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n r-zl2h9q"]'))
                            )
            i = 0
            flag = True
            while flag:
                post_element = post_elements[i]
                try:
                    post_element.click()
                    time.sleep(3)
                    tweet_link = self.driver.current_url
                    print(tweet_link)
                    if tweet_link not in self.tweet_links:
                        self.tweet_links.append(tweet_link)
                    back_btn = WebDriverWait(self.driver, self.medium_wait).until(
                                                EC.presence_of_element_located(
                                                    (By.XPATH, '//div[@aria-label="Back"]'))
                                            )
                    back_btn.click()
                    time.sleep(3)
                except Exception as e:
                    print(e)
                post_elements = WebDriverWait(self.driver, self.medium_wait).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n r-zl2h9q"]'))
                )

                i = i+1
                if i < len(post_elements):
                    flag=True
                else:
                    flag=False
            elements = WebDriverWait(self.driver, self.medium_wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@data-testid="cellInnerDiv"]'))
            )
            element = elements[-1]
            text = element.get_attribute('style')
            text = re.search(r"\((\w+)\)", text)
            text = text.group(0)
            px = int(''.join(filter(str.isdigit, text)))
            if px > self.px:
                self.px = px
                print(self.px)
            else:
                self.px = self.px + 717
                print(self.px)
            self.driver.execute_script(f"window.scrollTo(0, {self.px})")
        self.save_to_json()

    def get_tweet_data(self):
        file_name = f"{self.info_path}/link.json"
        with open(file_name, 'r', encoding='utf-8') as file:
            links = json.load(file)
        for link in links:
            self.open_link_new_tab(link)
            self.extract_data()
            self.close_new_tab()
            time.sleep(self.wait)
        pass

    def extract_data(self):
        print("link opened")
        time.sleep(self.wait)