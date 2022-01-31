#!/usr/local/bin/python3.10
######## FIRST THING TO DO ############################################
# Modify the previous line with your own python settings
#######################################################################
# BITBOT - Open Source Crypto Bot Trading Binance Api Based
# Software Released as GPL 3
#
# If you want to contribute please contact me at oculus@oculus.it 
#######################################################################
# DON'T USE THIS SOFTWARE WITH REAL CRYPTOS, IT IS IN PRE-PRE-PRE-ALPHA 
# TESTING. YOU CAN LOSE YOUR MONEY.
#######################################################################


######## TO DO ########################################################
## nothing to check
#######################################################################

import configparser
import requests
import time
import json
import os
import telebot
#import sys
#from pynput import keyboard
from datetime import datetime

######## RELEASE VERSION ##############################################
rel = "0.0.001 - ** TELEGRAM CHAT BOT **"

#######################################################################
######## CONFIGURATION VARIABLES ######################################
#######################################################################
scrypto = "BTC"
sfiat   = "USDT"
symbol  = scrypto + sfiat
configfile = "/etc/bitbot/"+symbol+".config"
#######################################################################

######## DEFINING COLOURS #############################################
class colore:
  verde = '\033[92m'
  rosso = '\033[91m'
  giall = '\033[93m'
  reset = '\033[0m'
  black = '\033[30m'
  red = '\033[31m'
  green = '\033[32m'
  orange = '\033[33m'
  blue = '\033[34m'
  purple = '\033[35m'
  cyan = '\033[36m'
  lightgrey = '\033[37m'
  darkgrey = '\033[90m'
  lightred = '\033[91m'
  lightgreen = '\033[92m'
  yellow = '\033[93m'
  lightblue = '\033[94m'
  pink = '\033[95m'
  lightcyan = '\033[96m'
  
def LeggiSaving():
 global guadagno, guadagnototale, totalebitacquistati, comprato, media, symbol, gainav, lossav, gainpc, losspc, gaincn, losscn, gainsm, losssm, prezzomedio, numeroacquisti
 global comm_last, comm_total, up, down
 config = configparser.ConfigParser()
 config.read_file(open(r'' + symbol + ".sav"))
 guadagno = float(config.get('saving', 'guadagno'))
 guadagnototale = float(config.get('saving', 'guadagnototale'))
 totalebitacquistati = float(config.get('saving', 'totalebitacquistati'))
 comprato = float(config.get('saving', 'comprato'))
 media = float(config.get('saving', 'media'))
 prezzomedio = float(config.get('saving', 'prezzomedio'))
 numeroacquisti = int(config.get('saving', 'numeroacquisti'))
 gainav = float(config.get('saving', 'gainav'))
 lossav = float(config.get('saving', 'lossav'))
 gainpc = float(config.get('saving', 'gainpc'))
 losspc = float(config.get('saving', 'losspc'))
 gaincn = float(config.get('saving', 'gaincn'))
 losscn = float(config.get('saving', 'losscn'))
 gainsm = float(config.get('saving', 'gainsm'))
 losssm = float(config.get('saving', 'losssm'))
 comm_last = float(config.get('saving', 'comm_last'))
 comm_total = float(config.get('saving', 'comm_total'))
 up = int(config.get('saving', 'up'))
 down = int(config.get('saving', 'down'))
 return True
 
def LeggiConfig(modo):
 global api, sek, fiat, maxfiat, limite, pausa, ferma, nonvendo, configfile, testneturl, gainpc, losspc, debugge, maxnonvendo, telegramtoken, telegramchatid, location, telegramnotify
 config = configparser.ConfigParser()
 config.read_file(open(r''+configfile))
 if modo == 1:
  api = config.get('binance', 'api')
  sek = config.get('binance', 'sek')
  testneturl = config.get('binance', 'testneturl')
  maxnonvendo = int(config.get('Var', 'maxsell'))
  debugge = int(config.get('Var', 'debug'))
  mingain = float(config.get('Var', 'mingain'))
  telegramtoken = config.get('telegram', 'token')
  telegramchatid = config.get('telegram', 'chatid')
  telegramnotify = int(config.get('telegram', 'notify'))
 if modo == 2:
  fiat = int(config.get('Var', 'fiat'))
  ferma = int(config.get('Var', 'stop'))
  maxfiat = int(config.get('Var', 'maxfiat'))
  pausa = int(config.get('Var', 'pause'))
  debugge = int(config.get('Var', 'debug'))
  mingain = float(config.get('Var', 'mingain'))
  telegramnotify = int(config.get('telegram', 'notify'))
 if modo == 3:
  fiat = int(config.get('Var', 'fiat'))
  ferma = int(config.get('Var', 'stop'))
  maxfiat = int(config.get('Var', 'maxfiat'))
  limite = int(config.get('Var', 'limit'))
  pausa = int(config.get('Var', 'pause'))
  maxnonvendo = int(config.get('Var', 'maxsell'))
  debugge = int(config.get('Var', 'debug'))
  gainpc = float(config.get('Var', 'gainpc'))
  losspc = float(config.get('Var', 'losspc'))
  mingain = float(config.get('Var', 'mingain'))
  telegramtoken = config.get('telegram', 'token')
  telegramchatid = config.get('telegram', 'chatid')
  location = config.get('Var', 'location')
  telegramnotify = int(config.get('telegram', 'notify'))
  comm_buy = float(config.get('binance', 'comm_buy'))
  comm_sell = float(config.get('binance', 'comm_sell'))
 if modo == 4:
  losspc = float(config.get('Var', 'losspc'))

LeggiConfig(3)
bot = telebot.TeleBot(telegramtoken)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	
bot.infinity_polling()
