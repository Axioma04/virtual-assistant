"""
Some basic assistant functionalities are protected in this file.

Contributors -> back-end developer & bug fixer : violence aka FurkanE
"""

# Clock information, current locale

import datetime
import requests
import math

from mtranslate import translate


# Transform, get now 

def get_current_clock() -> str:
    now = datetime.datetime.now()
    return now.strftime('%H %M')

# Simulate it and send to the main file 

def simulate_current_clock() -> str:
    hour, min = get_current_clock().split(' ')
    spokenText = ''
    # 15.00 -> on beş çift sıfır
    if min == '0' or min == '00':
        spokenText = f'{hour} çift sıfır'
    # 15.15 -> çeyrek geçiyor
    else:
        spokenText = f'{hour} {min}'
    return spokenText
    
# Economic Stuff (x dollars how much liras)

def get_aved(from_ = 'USD', to = 'TRY', amount = 1, accessKey = 'f7c8954643c7f3237fc55942915ce1b9359512f4', unformatted_from = '', unformatted_to = '') -> str:
    reqResponse = requests.get(f'https://api.getgeoapi.com/v2/currency/convert?api_key={accessKey}&from={from_}&to={to}')
    reqJSON = reqResponse.json()
    rate = round(float(reqJSON['rates'][to]['rate']) * amount, 2)
    print(rate)
    return f'{amount} {unformatted_from}, yaklaşık {rate} {unformatted_to} ediyor.' if rate != None else 'Bir hata meydana geldi'

# Day of the week, piece o cake

def get_day_of_the_week():
    now = datetime.datetime.now()
    day_of_the_week = translate(now.strftime('%A'), 'tr')
    return f'Bugün günlerden {day_of_the_week}'

# Current / Device Location

def get_device_credentials():
    response = requests.get('http://ipinfo.io/json').json()
    IP_, city, country = response['ip'], response['city'], response['country']
    return IP_, city, country 

def get_location() -> str:
    _, city, country = get_device_credentials()
    country = translate(country, 'tr')
    return f'{city} şehrinde bulunuyorsun.'

# Current Weather Detection

def get_weather_condition() -> str:
    _, city, _ = get_device_credentials()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=70ced96351e1eaaa25eeee8359b0ea81').json()
    condition = response['weather'][0]['main']
    condition = translate(condition, 'tr')
    temp = int(response['main']['temp'] - 273.15)
    return f'{city}\'da hava {condition} ve sıcaklık {temp} derece'