from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

chrome = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome)
driver.get("https://www.python.org")
time.sleep(3)
print(driver.title)
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("Is it love or just Python?")
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)
time.sleep(10)
driver.close()