from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support import Select
from selenium.common.exceptions import TimeoutException
import time
import mysql.connector

"""
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-02.cleardb.net'
app.config['MYSQL_USER'] = 'b8a30b72c2b3f4'
app.config['MYSQL_PASSWORD'] = '17088485'
app.config['MYSQL_DB'] = 'heroku_6c79d3633a7e6ba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
"""

#Configuration for the mysql
"""
mydb = mysql.connector.connect(
  host="us-cdbr-iron-east-02.cleardb.net",
  user="b8a30b72c2b3f4",
  passwd="17088485",
  database="heroku_6c79d3633a7e6ba"
)
"""
#mycursor = mydb.cursor(buffered=True)

def scrapefood():
    mydb = mysql.connector.connect(
      host="us-cdbr-iron-east-02.cleardb.net",
      user="b8a30b72c2b3f4",
      passwd="17088485",
      database="heroku_6c79d3633a7e6ba"
    )
    mycursor = mydb.cursor(buffered=True)
    #mycursor.execute("SET GLOBAL connect_timeout=28800")

    # Specifying incognito mode as you launch your browser[OPTIONAL]
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    # Create new Instance of Chrome in incognito mode
    browser = webdriver.Chrome()
    # Go to desired website
    browser.get("https://www.dineoncampus.com/trinity/whats-on-the-menu")

    time.sleep(15)

    a = browser.find_element_by_xpath('//input[@type = "search"]')
    a.click()
    time.sleep(15)
    b = browser.find_elements_by_xpath('//ul[@class="dropdown-menu"]/li/a')
    b[1].click()
    time.sleep(15)
    c = browser.find_elements_by_xpath('//li[@role = "presentation"]/a')
    c[0].click()
    time.sleep(15)
    titles_element = browser.find_elements_by_tag_name("strong")
    for menu in titles_element:
        if menu.text != "":
            sql = "INSERT INTO menu (food,time,location) VALUES (%s, %s, %s)"
            val = (menu.text,"breakfast","mather")
            mycursor.execute(sql, val)
            mydb.commit()

    c[1].click()
    time.sleep(10)
    titles_element = browser.find_elements_by_tag_name("strong")
    for menu in titles_element:
        if menu.text != "":
            mycursor = mydb.cursor(buffered=True)
            sql = "INSERT INTO menu (food,time,location) VALUES (%s, %s, %s)"
            val = (menu.text,"lunch","mather")
            mycursor.execute(sql, val)
            mydb.commit()


    c[2].click()
    time.sleep(10)
    titles_element = browser.find_elements_by_tag_name("strong")
    for menu in titles_element:
        if menu.text != "":
            sql = "INSERT INTO menu (food,time,location) VALUES (%s, %s, %s)"
            val = (menu.text,"dinner","mather")
            mycursor.execute(sql, val)
            mydb.commit()


if __name__ == "__main__":
    scrapefood()
