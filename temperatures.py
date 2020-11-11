import pysftp
import pandas as pd
import os
import csv
import numpy as np
import glob

def data_colector():
    myHostname = 'raspberrypi'
    myUsername = "pi"
    myPassword = "Hehe250994"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:

        print("Connection succesfully stablished ... ")

        remote_path = '/home/pi/Desktop/weather_station/data'
        local_path ='data'

        sftp.get_d(remote_path,local_path)
        print('Data boli uspesne stiahnute z raspberry!')

def data_adjuster():
    os.chdir('data')
    zoz = ('Namerana teplota','Aktualna teplota','Teplota1 (00:00-06:00)','Teplota1 (06:00-12:00)','Teplota1 (12:00-18:00)','Teplota1 (18:00-24:00)', 'Teplota2 (00:00-06:00)','Teplota2 (06:00-12:00)','Teplota2 (12:00-18:00)','Teplota2 (18:00-24:00)','Teplota3 (00:00-06:00)','Teplota3 (06:00-12:00)','Teplota3 (12:00-18:00)','Teplota3 (18:00-24:00)','Teplota4 (00:00-06:00)','Teplota4 (06:00-12:00)','Teplota4 (12:00-18:00)','Teplota4 (18:00-24:00)','Teplota5 (00:00-06:00)','Teplota5 (06:00-12:00)','Teplota5 (12:00-18:00)','Teplota5 (18:00-24:00)','Cas')
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    c = []
    for f in all_filenames:
        cch = (pd.read_csv(f))
        cch.columns = zoz
        c.append(cch)
    raw = pd.concat(c)

    i = 0
    empty = {}
    for element in zoz:
        empty[zoz[0]] = None
        if 0 < i < 22:
            raw[element] = raw[element].apply(lambda x: float(x.split('°')[0]))
        i += 1
    raw['Cas'] = pd.to_datetime(raw['Cas'], format="%H:%M:%S:%d:%m:%y")
    raw = raw.set_index('Cas')

    norma = raw.groupby(pd.Grouper(freq='10min')).mean()
    current_time = norma.last_valid_index()
    blank = pd.DataFrame(empty, index= pd.date_range(current_time, freq='10min',periods=720))
    blank = blank.drop(blank.index[1])
    norma = pd.concat([norma,blank])
    norma.drop([current_time], axis=0)

    strings = ('1_day_forecast', '2_day_forecast', '3_day_forecast', '4_day_forecast', '5_day_forecast')

    norma[strings[0]] = None
    norma[strings[1]] = None
    norma[strings[2]] = None
    norma[strings[3]] = None
    norma[strings[4]] = None

    for d in range(0,len(norma)-720,144):
        i = 0
        for z in range(2, len(zoz)-1,4):
            norma[strings[i]].loc[d:d+36] = norma[zoz[z]].iloc[[d,d+144]].mean()
            test0 = norma[zoz[z]].iloc[[d, d + 144]].mean()
            norma[strings[i]].loc[d+36:d+72] = norma[zoz[z+1]].iloc[[d, d + 144]].mean()
            test1 = norma[zoz[z+1]].iloc[[d, d + 144]].mean()
            norma[strings[i]].loc[d+72:d+108] = norma[zoz[z + 2]].iloc[[d, d + 144]].mean()
            test2 = norma[zoz[z + 2]].iloc[[d, d + 144]].mean()
            norma[strings[i]].loc[d+108:d+144] = norma[zoz[z + 3]].iloc[[d, d + 144]].mean()
            test3 = norma[zoz[z + 3]].iloc[[d, d + 144]].mean()
            i += 1
    norma[strings[0]] = norma[strings[0]].shift(periods=144)
    norma[strings[1]] = norma[strings[1]].shift(periods=2*144)
    norma[strings[2]] = norma[strings[2]].shift(periods=3*144)
    norma[strings[3]] = norma[strings[3]].shift(periods=4*144)
    norma[strings[4]] = norma[strings[4]].shift(periods=5*144)

    norma = norma.drop(list(zoz[2:22]), axis=1)

    return raw, norma

def main():

    data_colector()
    data,norma = data_adjuster()
    print(norma)
if __name__ == '__main__':
    main()



