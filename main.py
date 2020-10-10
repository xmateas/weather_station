import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
while True:
    response = requests.get('https://www.meteoblue.com/sk/po%C4%8Dasie/t%C3%BD%C5%BEde%C5%88/kysuck%c3%a9-nov%c3%a9-mesto_slovensko_3059179')
    soup = BeautifulSoup(response.text,'html.parser')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    el = soup.find(class_ = 'current_temp').get_text()
    el = (el.split('°')[0])[-3:-1]

    with open('temp_data.csv','a', encoding='utf-8', newline='') as temp_data:
        temp_writer = csv.writer(temp_data)
        temp_writer.writerow([el,current_time])

    time.sleep(100)

    from datetime import datetime
