import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import *

chrome_op = Options()
chrome_op.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
wd = webdriver.Chrome(options=chrome_op)

open_region = wd.find_element(By.XPATH, '//*[contains(@class,"public")]')

all_mask_region = wd.find_elements(By.XPATH, '//*[contains(@class,"mask")]')

all_unready_region = [WebElement]

for mask_region in all_mask_region:
    region = wd.find_element(locate_with(By.XPATH, '//*[contains(@class,"public")]').near(mask_region))
    region.click()
    
    wd.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", region, 'style', 'background: white')

