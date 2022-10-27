import time
import hashlib
from urllib import response
import requests
import json
from urllib.request import urlopen, Request
from songline import Sendline
import datetime
import pandas as pd


# setting the URL you want to monito
url = 'http://apidata.pm25vipa.tk/query?pretty=true&db=pm_dht_map_data&q=SELECT "pm2p5","pm10","temp","humid","name" FROM "databaseall"  GROUP BY * ORDER BY DESC LIMIT 1'

# to perform a GET request and load the
# content of the website and store it in a var
# response = requests.get(url)

# # to create the initial hash
# currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(10)

token = 'wTUellYiIIedSokhIIELR7WKIk6KmkPCZrMrxlWKE8V'


messenger = Sendline(token)


def _getSendNotify():

    url = 'http://apidata.pm25vipa.tk/query?pretty=true&db=pm_dht_map_data&q=SELECT "pm2p5","pm10","temp","humid","name" FROM "databaseall"  GROUP BY * ORDER BY DESC LIMIT 1'
    res = requests.get(url)
    data = json.loads(res.text)

    # print(data)
    temp = data['results'][0]['series'][0]['values']
    new_temp = temp[0][3]

    humid = data['results'][0]['series'][0]['values']
    new_humid = humid[0][4]

    pm2p5 = data['results'][0]['series'][0]['values']
    new_pm2p5 = pm2p5[0][1]

    pm10 = data['results'][0]['series'][0]['values']
    new_pm10 = pm10[0][2]

    name = data['results'][0]['series'][0]['values']
    new_name = name[0][5]

    # %d-%m-%Y %H:%M
    # 2022-01-28 00:16:54
    currentTime = data['results'][0]['series'][0]['values']
    new_datetime = currentTime[0][0]
    new_time = pd.to_datetime(new_datetime).tz_convert('Asia/Bangkok')
    s = str(new_time)
    convert_time = s[:19]
    new_convert_time = datetime.datetime.strptime(
        convert_time, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')

    print(new_temp, new_humid, new_convert_time)

    if float(new_temp) > 15:
        messenger.sendtext('\n' + '🟢' + 'ส่งแจ้งเตือนสถานีที่วัดฝุ่น' + '\n' + '🟢'
                           + '\n' + '\n' +
                           '🔔สถานี: ' + str(new_name) + ' 🔴' + '\n' +
                           '🌡อุณหภูมิ: ' + str(new_temp) + ' C' + ' 🔴' + '\n' +
                           '🌧ความชื้น: ' + str(new_humid) + ' %' + ' 🔴' + '\n' +
                           '💨pm2.5: ' + str(new_pm2p5) + ' µg./m3' + ' 🔴' + '\n' +
                           '💨pm10: ' + str(new_pm10) + ' µg./m3' + ' 🔴' + '\n' +
                           '⏰เวลา: ' + str(new_convert_time) + '\n'
                           )
    print("ส่งแจ้งเตือนค่าอุณหภูมิ:" + str(new_temp) + "เกินนะ")


while True:
    try:
                        # perform the get request and store it in a var
        res = requests.get(url)

                   # create a hash
        currentHash = json.loads(res.text)

        # wait for 30 seconds
        time.sleep(15)

         # perform the get request
        res = requests.get(url)

          # create a new hash
        newHash = json.loads(res.text)

           # check if new hash is same as the previous hash
        if newHash == currentHash:
            continue

                # if something changed in the hashes
        else:
                _getSendNotify()

                # again read the website
                res = requests.get(url)

                # create a hash
                currentHash = json.loads(res.text)

                # wait for 30 second
                time.sleep(15) #10
                continue

    # To handle exceptions
    except Exception as e:
        print('error')
