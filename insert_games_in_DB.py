import sqlite3
from selenium.webdriver.firefox.service import Service
import time
from datetime import datetime
import steamDB
from bs4 import BeautifulSoup

count = 1
plataform = 'Pc'
conn = sqlite3.connect('steamDB.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS steamDB
             (id INTEGER PRIMARY KEY, url TEXT, html TEXT, plataform TEXT, timestamp DATETIME)''')


def get_file_length():
    with open('links.txt', 'r') as file:
        line = file.readlines()
        length = line[-1]
    return length


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def start():
    global count 
    i=0
    j=0
    lista =[]
    #iniciate the scrapping
    #steamDB.initiate()
    length = get_file_length()
    print(length)
    #open the file
    with open('links.txt','r') as file:
        while (i<int(length)):
            lista.append(file.readline())
            i+=1
    #to drible the bot searcher need to open a browser to each one link we have (1878 links)
    while j< len(lista):
        #time out to not get banned from Steam DB
        if(count % 300 == 0):
            print("stop")
            time.sleep(3600)
        #get the Driver to navegate to all links
        driver = steamDB.drive_initiate()
        print(lista[j])
        #go to an site of the list
        page = driver.get(lista[j])
        #get all html
        html = driver.page_source
        #parse the html
        soup = BeautifulSoup(html,'html.parser')
        #get the url in the html
        url = soup.find_all("nav", "app-links")
        url = str(url)
        soups = BeautifulSoup(url,'html.parser')
        url = soups.find("a")
        #get the tile in the html
        title = soup.find("h1")

        #get the price in the html
        price = soup.find("tr","table-prices-current")
        price = str(price)
        soupo = BeautifulSoup(price,'html.parser')
        price = soupo.find_all('td')
        soupo = str(soupo)
        info = ''
        info += str(title)
        if(soupo != 'None'):
            info += str(price[1])
        time.sleep(1)
        #save the informations in a DB called steamDB
        c.execute("INSERT INTO steamDB (url, html, plataform, timestamp ) VALUES ( ?, ?, ?, ?)", (url.get('href'), info, plataform, get_current_time()))
        conn.commit()
        driver.close()
        j+=1
        count+=1
        print(j)
        print(' ')
        time.sleep(6)
    conn.close()


start()

