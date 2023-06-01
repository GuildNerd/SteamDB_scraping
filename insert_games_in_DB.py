import sqlite3
from selenium.webdriver.firefox.service import Service
import time
from datetime import datetime
from steamDB import drive_iniciate 
from bs4 import BeautifulSoup


plataform = 'Pc'
conn = sqlite3.connect('documents_html.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS documents_html
             (id INTEGER PRIMARY KEY, url TEXT, html TEXT, plataform TEXT, timestamp DATETIME)''')


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

i=0
j=0
lista =[]
with open('fe.txt','r') as file:
    while (i<1878):
        lista.append(file.readline())
        i+=1
       
 
#to drible the bot searcher need to open a browser to each one link we have (1878 links)
while j< len(lista):
    #get the Driver to navegate to all links
    driver = drive_iniciate()
    print(lista[j])
    #go to an site of the list
    page = driver.get(lista[j])
    #get all html
    html = driver.page_source
    #parse the html
    soup = BeautifulSoup(html,'html.parser')
    #get the body in the html
    bod = soup.find_all('body','en_US')
    body = str(bod)

    time.sleep(3)
    #save the informations in a DB called documents
    c.execute("INSERT INTO documents_html (url, html, plataform, timestamp ) VALUES ( ?, ?, ?, ?)", (lista[j], body, plataform, get_current_time()))
    conn.commit()
    driver.close()
    j+=1

conn.close()
