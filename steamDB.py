from selenium import webdriver
import sqlite3
from bs4 import BeautifulSoup
import time


#conn = sqlite3.connect('documentis_html.db')
#c = conn.cursor()
#c.execute('''CREATE TABLE IF NOT EXISTS documentis_html
             #(id INTEGER PRIMARY KEY, url TEXT, html TEXT, plataform TEXT)''')

# initiate the drive to navigate on web
def drive_initiate():
    driver = webdriver.Chrome()
    return driver


# with the page open, get the root page
def get_root_page(driver):
    # Navigate to the webpage
    driver.get('https://steamdb.info/charts/')
    time.sleep(5)
    # Extract the HTML from the webpage
    html = driver.page_source
    return html


# parse the html and gets all 'td.a' (html table items)
def get_child_pages(html):
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # listed games
    infos = soup.find_all("td>a")
    links = []
    # append all the links of the game pages
    for info in infos:
        gamePageUrl = "https://steamdb.info"+info.get("href")
        gamePageUrl = gamePageUrl[0:-7]
        links.append(str(gamePageUrl))
    return links


# main function
def initiate():
    driver = drive_initiate()
    rootpage = get_root_page(driver)
    childpages = get_child_pages(rootpage)

    i = 0
    while (i<5):
        time.sleep(2)
        print(childpages[i])

    driver.quit()
    
initiate()

# Close the Selenium webdriver

#conn.close()