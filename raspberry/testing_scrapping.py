import csv
from datetime import datetime as dt
import os
import glob
import requests
from bs4 import BeautifulSoup
import time
from time import process_time


def scrapper():
    zoz = []
    response1 = requests.get('https://www.meteoblue.com/sk/po%C4%8Dasie/t%C3%BD%C5%BEde%C5%88/kysuck%c3%a9-nov%c3%a9-mesto_slovensko_3059179')
    soup = BeautifulSoup(response1.text, 'html.parser')

    el = soup.find(class_='current_temp').get_text()
    el = (el.split(u'\u00b0')[0])[-3:-1] + '°'

    response2 = requests.get('https://www.yr.no/place/Slovakia/%C5%BDilina/Kysuck%C3%A9_Nov%C3%A9_Mesto/long.html')
    soup = BeautifulSoup(response2.text, 'html.parser')
    z = soup.find_all(class_='temperature plus')
    # print(type(z))
    i = 0
    for index in z:
        i += 1
        if 9 < i < 30:
            zoz.append(index.get_text())
        else:
            continue
        # if len(zoz) == 5:
        #     break

    zoz.insert(0,el)
    return zoz

start = process_time()
result = scrapper()
finish = process_time()

print('Proces time',finish-start)


print(result)
