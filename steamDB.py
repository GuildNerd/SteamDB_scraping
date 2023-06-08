from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

lines=0


# initiate the drive to navigate on web
def drive_initiate():
    FFdriver = '/snap/firefox/2667/usr/lib/firefox/geckodriver'
    firefox = '/snap/firefox/2667/usr/lib/firefox/firefox'


    service = Service(executable_path = FFdriver)
    # Set up the Selenium webdriver
    driver = webdriver.Firefox(service = service, firefox_binary = firefox)
    return driver


# with the page open, get the root page
def get_root_page(driver):
    
    time.sleep(5)
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
        gamePageUrl = "https://steamdb.info"+info.get("href")
        gamePageUrl = gamePageUrl[0:-7]
        links.append(str(gamePageUrl))
    return links

def next_page( driver):
    # Navigate to the webpage
    driver.get('https://steamdb.info/charts/')
    button = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/label/select/option[7]")
    button.click()
 

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
    next_page(driver)
    time.sleep(2)
    rootpage = get_root_page(driver)
    childpages = get_child_pages(rootpage)
    write(childpages)
    write_number_of_lines()

    # Close the Selenium webdriver
    driver.quit()


