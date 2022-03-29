"""
The events when just be executed, when the assistant first activated.

Contributors -> back-end developer & bug fixer : violence aka FurkanE
"""

import json 
import os
import re
import multiprocessing

from random import choice
from pynput.keyboard import Key, Controller, Listener
from playsound import playsound
from responses import target
from time import sleep

import basic_funcs as basic
import gtts_spr_main as gtspr

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_FOLDER = os.path.dirname(os.path.dirname(BASE_DIR))
PUBLIC_FOLDER = MAIN_FOLDER + '\public'
SOUNDS_FOLDER = PUBLIC_FOLDER + '\sounds'
CONFIG_FOLDER = PUBLIC_FOLDER + '\configs'
PROCESSES = []
PRIMARY_PROCESSES = ['', '', '']
inputStarted = False
inputUser = ''

with open(CONFIG_FOLDER + '/main_config.json') as jsonFile:
    jsonDictContent = json.loads(jsonFile.read())

# Send the first message outloud. Retrieve messages from main config, public file.

def send_welcome_message() -> None:
    selected_message = choice(jsonDictContent['firstmsgs']['knownUser'])
    gtspr.speak(selected_message, 'tr')
    say_things_can_be_done()

# Things that the assistant can do.

def say_things_can_be_done() -> None:
    selected_thing = choice(jsonDictContent['firstmsgs']['thingsCanBeDone'])
    gtspr.speak(f'Beni test etmek için {selected_thing} diyebilirsin. Yapabileceğim her şeyi görmek için neler yapabileceğimi sorabilirsin.', 'tr')

# Terminate all processes

def terminateAll():
    for process in PROCESSES:
        process.terminate()
# debugger json

def validator_json(jsono) -> None:
    dictObj = json.loads(jsono)
    converted = json.dumps(dictObj)
    print(converted)


def on_press(key):
    global inputStarted, SOUNDS_FOLDER
    if key == Key.ctrl_l and inputStarted == False:
        terminateAll()
        print(inputStarted)
        BG_TASK = multiprocessing.Process(target=playsound, args=(SOUNDS_FOLDER + '/open.mp3',)) #playsound(SOUNDS_FOLDER + '/open.mp3')
        BG_TASK.start()
        inputUser = gtspr.record()
        inputStarted = True 
        BG_TASK.terminate()
        decide(inputUser)
        BG_TASK = multiprocessing.Process(target=playsound, args=(SOUNDS_FOLDER + '/close.mp3',))
        BG_TASK.start()
        inputUser = ''
        sleep(3)
        BG_TASK.terminate()
        del BG_TASK
        inputStarted = False
#main loop
    
CURRENCY_ABBRS = {'dolar': 'USD', 'dölar': 'USD', 'dalar': 'USD', 'dalır': 'USD', 'oyro': 'EUR', 'yuro': 'EUR', 'euro': 'EUR', 'tele': 'TRY', 'tl': 'TRY', 'türk lirası': 'TRY', 'Türk Lirası': 'TRY', 'Sterlin': 'GBP', 'Pound': 'GBP'}

def decide(inputUser):
    if re.search('saat', inputUser):
        # Clock simulation
        clockRequest = basic.simulate_current_clock()
        gtspr.speak(f'Şu anda saat {clockRequest}, Sana başka nasıl yardımcı olabilirim?')
    elif re.search('dolar|euro|tl|tele|türk lirası|oyro', inputUser):
        # Currency simulation
        if re.search('kaç|ne kadar', inputUser):
            words = inputUser.split(' ')
            to = from_ = amount = 0
            for word in words:
                if word != 'kaç' and word != 'ne kadar' and word != 'eder' and word != 'etmekte':
                    if word.isdigit():
                        if amount == 0:
                            amount = int(word)
                    else:
                        if from_ == 0:
                            from_ = word 
                        else:
                            to = word 
            old_to, old_from = to, from_
            for key, val in CURRENCY_ABBRS.items():
                if key.lower() == to.lower(): 
                    to = val 
                if key.lower() == from_.lower():
                    from_ = val
            currencyRequest = basic.get_aved(from_, to, amount, unformatted_from=old_from, unformatted_to=old_to)
            gtspr.speak(currencyRequest)
    elif re.search('bugün günlerden ne|günlerden ne|haftanın günü', inputUser):
        # Day of the week
        dayOfTheWeekRequest = basic.get_day_of_the_week()
        gtspr.speak(dayOfTheWeekRequest)
    elif re.search('genel konum|şehir|ülke', inputUser):
        # General Location, with API
        geoLOC = basic.get_location()
        gtspr.speak(geoLOC)
    elif re.search('hava', inputUser):
        # Current weather, with API
        specificTime = inputUser.split('hava')[1]
        weatherREQ = basic.get_weather_condition()
        gtspr.speak(weatherREQ)



# Never closing program

def Protecter():
    while 1: 
        pass

# Key bug fixer

# GTTS & SRP

# Main call

if __name__ == '__main__':
    keyboard = Controller()
    PROCESSES.append(multiprocessing.Process(target=send_welcome_message))
    PROCESSES[0].start()
    inputStarted = False
    PRIMARY_PROCESSES.insert(2, multiprocessing.Process(target=Protecter))
    PRIMARY_PROCESSES[2].start()
    with Listener(on_press=on_press) as listener:
        listener.join()

