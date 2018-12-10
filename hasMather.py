from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support import Select
from selenium.common.exceptions import TimeoutException
import time

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome()

# Go to desired website
browser.get("https://www.dineoncampus.com/trinity/whats-on-the-menu")

mather = []
bistro = []
cave = []


# Get all of the titles for the pinned repositories
# We are not just getting pure titles but we are getting a selenium object
# with selenium elements of the titles.

# find_elements_by_xpath - Returns an array of selenium objects.
#titles_element = browser.find_elements_by_xpath("//table[@class='menu-items']")
time.sleep(5)

a = browser.find_element_by_xpath('//input[@type = "search"]')
a.click()
time.sleep(10)
b = browser.find_elements_by_xpath('//ul[@class="dropdown-menu"]/li/a')
b[1].click()
time.sleep(10)
c = browser.find_elements_by_xpath('//li[@role = "presentation"]/a')
c[0].click()
time.sleep(10)
titles_element = browser.find_elements_by_tag_name("strong")
for menu in titles_element:
    if menu.text != "":
        mather.append(menu)
        print(menu.text)

c[1].click()
time.sleep(10)
titles_element = browser.find_elements_by_tag_name("strong")
for menu in titles_element:
    if menu.text != "":
        print(menu.text)
        mather.append(menu)

c[2].click()
time.sleep(10)
titles_element = browser.find_elements_by_tag_name("strong")
for menu in titles_element:
    if menu.text != "":
        print(menu.text)
        mather.append(menu)


def  hasFood(food):
   for i in mather:
       if i == food:
           return 0
   return 1
print(hasFood("Clam Chowder"))
