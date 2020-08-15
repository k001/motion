#!/usr/bin/python2
import datetime
import telepot
import time
import requests
import os
import glob
import psutil
from telepot.loop import MessageLoop
from decimal import Decimal
#obtenerinformacion sobre mi cuenta/bot
#https://api.telegram.org/bot1234:ASJLASDUIQNASFD/getUpdates
#bot=telepot.Bot('1234:ASJLASDUIQNASFD') #enrolar a mi bot
#chat_id=654321 #enrolar a mi chat
#bot.getMe() #obtiene la informacion del bot
#bot.sendPhoto(654321, photo=open('./CAM1_36-20200402102522-01.jpg', 'rb'))  #envia una image

def webcontrol(chat_id, type, cmd):
    req = 'http://localhost:8081/0/'+type+'/'+cmd
    res = requests.get(req)
    bot.sendMessage(chat_id, res.text)

def serviceStatus(chat_id):
    status = [os.system('service motion status'), os.system('service motioneye status')]
    if status[0] == 0:
        bot.sendMessage(chat_id, ('motion is running'))
    else:
        bot.sendMessage(chat_id, ('motion is Not running'))
    if status[1] == 0:
        bot.sendMessage(chat_id, ('motionEye is running'))
    else:
        bot.sendMessage(chat_id, ('motionEye is Not running'))

def sendMultimedia(chat_id, command):
    if command == '/snapshot':
        try:
            photo = max(glob.iglob('/sharedfolders/Motioneye/*.jpg'), key=os.path.getctime)
            bot.sendPhoto(chat_id, photo=open(photo, 'rb'), caption='last photo')
        except(ValueError, TypeError):
            bot.sendMessage(chat_id, ('No hay photos para enviar'))
    else:
        try:
            video = max(glob.iglob('/sharedfolders/Motioneye/*.avi'), key=os.path.getctime)
            bot.sendVideo(chat_id, video=open(video, 'rb'), caption='last video')
        except(ValueError, TypeError):
            bot.sendMessage(chat_id, ('No hay videos para enviar'))

def startMotion(chat_id):
    os.system('sudo service motion start')
    serviceStatus(chat_id)

def stopMotion(chat_id):
    os.system('sudo service motion stop')
    serviceStatus(chat_id)

def powerOff(chat_id):
    bot.sendMessage(chat_id, ('Hasta la vista baby!...'))
    os.system('sudo shutdown -h now')

def check(chat_id):
    hddroot = psutil.disk_usage('/')
    try:
        bot.sendMessage(chat_id, ('Particion /'))
        bot.sendMessage(chat_id, ('Total en GB: ' + str(round(hddroot.total/(1024.0 ** 3),2))))
        bot.sendMessage(chat_id, ('Used en GB: ' + str(round(hddroot.used/(1024 ** 3),2))))
        bot.sendMessage(chat_id, ('Free en GB: ' + str(round(hddroot.free / (1024 ** 3),2))))
    except(ValueError, TypeError):
        bot.sendMessage(chat_id, ('No se pudo leer la particion / '))


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    #should work thanks to Winston
    print(msg['from']['id'])
    if msg['from']['id'] != 654321:
        bot.sendMessage(chat_id, "Este es un bot personal largate de aqui. Acceso Denegado!")
        exit(1)
    print 'Got command: %s' % command
    if command == '/snapshot':
        sendMultimedia(chat_id, command)
    elif command == '/status':
        serviceStatus(chat_id)
    elif command == '/check':
        check(chat_id)
        #webcontrol(chat_id, 'detection', 'connection')
    elif command == '/start':
        startMotion(chat_id)
    elif command == '/stop':
        stopMotion(chat_id)
    elif command == '/poweroff':
        powerOff(chat_id)
    elif command == '/video':
        sendMultimedia(chat_id, command)
    else:
        bot.sendMessage(chat_id, "No te entendi, no reconozco este comando: "+command)
# adapt the following to the bot_id:bot_token
bot = telepot.Bot('1234:ASJLASDUIQNASFD')
MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'
while 1:
    time.sleep(10)