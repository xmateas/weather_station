import csv
from datetime import datetime as dt
import os
import glob
import requests
from bs4 import BeautifulSoup
import time
#import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # setovanie LED
GPIO.setup(18, GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    pass

def read_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    #lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
       time.sleep(0.2)
       lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
       temp_string = lines[1][equals_pos + 2:]
       temp_c = float(temp_string) / 1000.0

    return temp_c


def scrapper():
    zoz = []
    response1 = requests.get('https://www.meteoblue.com/sk/po%C4%8Dasie/t%C3%BD%C5%BEde%C5%88/kysuck%c3%a9-nov%c3%a9-mesto_slovensko_3059179')
    soup = BeautifulSoup(response1.text, 'html.parser')

    el = soup.find(class_='current_temp').get_text()
    el = (el.split(u'\u00b0')[0])[-3:-1] + '°'

    response2 = requests.get('https://www.yr.no/place/Slovakia/%C5%BDilina/Kysuck%C3%A9_Nov%C3%A9_Mesto/long.html')
    soup = BeautifulSoup(response2.text, 'html.parser')
    z = soup.find_all(class_='temperature plus')

    i = 0
    for index in z:
        i += 1
        if 9 < i < 30:
            zoz.append(index.get_text())
        else:
            continue
    zoz.insert(0,el)
    return zoz



def data_writer(datum):
    dir = 'data/'
    with open((dir + (datum + '.csv')), 'a', encoding='utf-8', newline='') as temp_data:
        net = scrapper()
        real = read_temp()
        now = dt.now()
        current_time = now.strftime("%H:%M:%S")
        temp_writer = csv.writer(temp_data)
        temp_writer.writerow([real,net[0],net[1],net[2],net[3],net[4],net[5], current_time]) # format ulozenia: namerane data;dnes; o 1 den, o 2 dni; o3 dni; o 4 dni; o 5 dni
        print('Internetova teplota: ' + net[0])
        print('Namerana teplota: ' + str(real))



def main():
    day = (dt.now()).day
    dat_acc = (dt.now()).day
    while 1:
        while day == dat_acc:

            name_file = dt.now().strftime('%d.%m.%Y')

            GPIO.output(18, GPIO.HIGH)
            data_writer(name_file)
            GPIO.output(18, GPIO.LOW)

            day = (dt.now()).day
            time.sleep(120)

        dat_acc = (dt.now()).day

if __name__ == "__main__":
    main()


##
import csv
from datetime import datetime as dt
import os
import glob
import requests
from bs4 import BeautifulSoup
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # setovanie LED
GPIO.setup(18, GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    pass


def read_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    # lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0

    return temp_c


def scrapper():
    zoz = []
    response1 = requests.get(
        'https://www.meteoblue.com/sk/po%C4%8Dasie/t%C3%BD%C5%BEde%C5%88/kysuck%c3%a9-nov%c3%a9-mesto_slovensko_3059179')
    soup = BeautifulSoup(response1.text, 'html.parser')

    el = soup.find(class_='current_temp').get_text()
    el = (el.split(u'\u00b0')[0])[-3:-1] + '°'

    response2 = requests.get('https://www.yr.no/place/Slovakia/%C5%BDilina/Kysuck%C3%A9_Nov%C3%A9_Mesto/long.html')
    soup = BeautifulSoup(response2.text, 'html.parser')
    z = soup.find_all(class_='temperature plus')
    i = 0
    for index in z:
        i += 1
        if 9 < i < 30:
            zoz.append(index.get_text())
        else:
            continue

    zoz.insert(0, el)
    return zoz


def data_writer(datum):
    dir = 'data/'
    with open(dir + (datum + '.csv'), 'a', encoding='utf-8', newline='') as temp_data:
        net = scrapper()
        real = read_temp()
        now = dt.now()
        current_time = now.strftime("%H:%M:%S:%d:%m:%y")
        temp_writer = csv.writer(temp_data)
        temp_writer.writerow(
            [real, net[0], net[1], net[2], net[3], net[4], net[5], net[6], net[7], net[8], net[9], net[10], net[11],
             net[12], net[13], net[14], net[15], net[16], net[17], net[18], net[19], net[20], current_time])
        print('Internetova teplota: ' + net[0])
        print('Namerana teplota: ' + str(real))


def main():
    day = (dt.now()).day
    dat_acc = (dt.now()).day
    while 1:
        while day == dat_acc:
            name_file = dt.now().strftime('%Y.%m.%d')

            GPIO.output(18, GPIO.HIGH)
            data_writer(name_file)
            GPIO.output(18, GPIO.LOW)

            day = (dt.now()).day
            time.sleep(120)

        dat_acc = (dt.now()).day


if __name__ == "__main__":
    main()
#
