from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from settings.config import ROOT_PATH, DATA_PATH, DRIVER_PATH, INFO_PATH
from twitter_scraper_class.twitter_scraper_class import TwitterScraper
from functions import make_dir


driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"
data_path = f"{ROOT_PATH}/{DATA_PATH}"
info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
make_dir(data_path)
make_dir(driver_path)
make_dir(info_path)

options = Options()
options.headless = False
chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

twitter_scraper = TwitterScraper(driver, data_path, info_path)