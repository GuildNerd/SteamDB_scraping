from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

lines=0
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
    time.sleep(30)
    # Extract the HTML from the webpage
    html = driver.page_source
    return html


# parse the html and gets all 'td.a' (html table items)
def get_child_pages(html):
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # listed games
    data = soup.find_all("td","applogo text-left")
    data = str(data)
    soup= BeautifulSoup(data,'html.parser')
    infos = soup.find_all('a') 
    links = []
    # append all the links of the game pages
    for info in infos:
        print(info)
        gamePageUrl = "https://steamdb.info"+info.get("href")
        gamePageUrl = gamePageUrl[0:-7]
        links.append(str(gamePageUrl))
    return links

def next_page(html, driver):
    i= 0
    childpages = get_child_pages(html)
    write(childpages)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(1)
    button = driver.find_element(By.ID,"table-apps_next")
    button.click()
    i+=1

#write all links in a .TXT
def write(list):
    count_lines = 0
    with open('links.txt', 'a') as f:
        for links in list:
            link = str(links)
            f.write(f'{links}\n')
            count_lines+=1
        global lines
        lines+=count_lines

def write_number_of_lines():
    with open('links.txt', 'a') as f:
        global lines

        f.write(str(lines))

# main function
def initiate():
    driver = drive_initiate()
    rootpage = get_root_page(driver)
    next_page(rootpage, driver)
    write_number_of_lines()

    driver.quit()
    


# Close the Selenium webdriver

#conn.close()