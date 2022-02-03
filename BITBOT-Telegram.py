#!/usr/local/bin/python3.10
######## FIRST THING TO DO ############################################
# Modify the previous line with your own python settings
#######################################################################
# BITBOT - Open Source Telegram Support for Crypto Bot Trading Binance
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
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

######## RELEASE VERSION ##############################################
rel = "0.0.011 - ** BITBOT TELEGRAM CHAT BOT **"

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
 ora = Ora()
 replymessage = "BITBOT - " + ora + "\nLatest situation"
 replymessage = replymessage + "\n\n- Last Gain: " + str(guadagno)
 replymessage = replymessage + "\n- Total Gain: " + str(guadagnototale)
 replymessage = replymessage + "\n- Total Crypto Bought: " + str(totalebitacquistati)
 replymessage = replymessage + "\n- Bought: " + str(comprato)
 replymessage = replymessage + "\n- Average: " + str(media)
 replymessage = replymessage + "\n- Last Commissions: " + str(comm_last)
 replymessage = replymessage + "\n- Total Commissions: " + str(comm_total)
 return replymessage
 
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

def Valore():
	global symbol
	try:
		response = client.get_symbol_ticker(symbol=symbol)
		attuale = float(response['price'])
		return attuale
	except:
		attuale = "Connection Error!"
		return attuale

def Ora():
 now = datetime.now()    
 dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
 return dt_string
 
def Saldo():
 global sfiat, scrypto
 # get balance for a specific asset only (BTC)
 ora = Ora()
 balancemessage = "BITBOT - " + ora + " - Actual Balance\n\n"
 balancemessage = balancemessage + "- USDT AVAILABLE: " + str(client.get_asset_balance(asset=sfiat)['free']) + "\n"
 balancemessage = balancemessage + " - " + scrypto + " AVAILABLE: " + str(client.get_asset_balance(asset=scrypto)['free']) + "\n"
 balancemessage = balancemessage + " - BNB  AVAILABLE: " + str(client.get_asset_balance(asset="BNB")['free'])
 return balancemessage

LeggiConfig(1)
LeggiConfig(3)

print(colore.verde)
print("  _______   _______   ___       _______   _______   _______   _______   ___ ___       _______    _______   _______ ")
print(" |       | |   _   | |   |     |   _   | |   _   | |   _   \ |   _   | |   Y   |     |   _   \  |   _   | |       |")
print(" |.|   | | |.  1___| |.  |     |.  1___| |.  |___| |.  l   / |.  1   | |.      |     |.  1   /  |.  |   | |.|   | |")
print(" `-|.  |-' |.  __)_  |.  |___  |.  __)_  |.  |   | |.  _   1 |.  _   | |. \_/  |     |.  _   \  |.  |   | `-|.  |-'")
print("   |:  |   |:  1   | |:  1   | |:  1   | |:  1   | |:  |   | |:  |   | |:  |   |     |:  1    \ |:  1   |   |:  |  ")
print("   |::.|   |::.. . | |::.. . | |::.. . | |::.. . | |::.|:. | |::.|:. | |::.|:. |     |::.. .  / |::.. . |   |::.|  ")
print("   `---'   `-------' `-------' `-------' `-------' `--- ---' `--- ---' `--- ---'     `-------'  `-------'   `---'  ")
print("                    C R Y P T O - A U T O T R A D E R - T E L E G R A M B O T   S U P P O R T                      ")
print("                                                  by Oculus.it                                                     ")
print(colore.giall + "\n  Release " + rel + colore.reset)
print("")

                                                                                                                   


if testneturl == "":
 testnet = 0
else:
 testnet = 1
 
##### CONNECT TO TELEGRAM
bot = telebot.TeleBot(telegramtoken)

######## CONNECT TO BINANCE ###########################################
try:
 client = Client(api, sek)
 if testnet == 1:
  client.API_URL = testneturl 
except:
 print("ERROR: Cannot connect to Binance APIs phase 1. Check your internet connection and your keys activation.")
 quit()

######## CONNECT TO THE ACCOUNT #######################################
try:
 client.get_account()
except:
 print("ERROR: Cannot connect to Binance APIs phase 2. Check your internet connection and your keys activation.")
 quit()

@bot.message_handler(commands=['start', 'via'])
def send_welcome(message):
	ora = Ora()
	print(ora + " - Welcome message sended\n\n")
	bot.reply_to(message, "Hi! Welcome to BITBOT Telegram configurator!\n\nUse /help command to khow commands available!")

@bot.message_handler(commands=['help', 'aiuto'])
def send_help(message):
	ora = Ora()
	aiuto = "BITBOT - " + ora + " - HELP ON LINE"
	aiuto = aiuto + "\n\nCOMMANDS AVAILABLE:"
	aiuto = aiuto + "\n- /start - Welcome message"
	aiuto = aiuto + "\n- /balance - Acutual crypto, stable and BNB balance"
	aiuto = aiuto + "\n- /latest - Latest saved values"
	aiuto = aiuto + "\n- /crypto - Actual crypto value"
	aiuto = aiuto + "\n\n\nMore commands will be implemented soon!"
	print(ora + " - Help message sended\n" + aiuto + "\n\n")
	bot.reply_to(message, aiuto)
	
@bot.message_handler(commands=['balance', 'saldo'])
def send_welcome(message):
	balancemessage = Saldo()
	ora = Ora()
	print(ora + " - Balance message sended\n" + balancemessage + "\n\n")
	bot.reply_to(message, balancemessage)
	
@bot.message_handler(commands=['crypto', 'cripto'])
def send_crypto(message):
	ora = Ora()
	actuale = Valore()
	cryptomessage = "BITBOT " +  ora + " - INSTANT CRYPTO VALUE " + symbol + "\n\n"
	cryptomessage = cryptomessage + "- " + str(actuale) + " " + sfiat
	print(ora + " - Crypto message sended\n" + cryptomessage + "\n\n")
	bot.reply_to(message, cryptomessage)
	
@bot.message_handler(commands=['latest', 'last-situation', 'ultimo-salvataggio'])
def send_situation(message):
	ora = Ora()
	situazione = LeggiSaving()
	print(ora + " - Latest message sended\n" + situazione + "\n\n")
	bot.reply_to(message, situazione)
	
#@bot.message_handler(commands=['set'])
#def send_set(message):
#	message = message.replace("/set ", "")
#	print("You want to set the following variable: >" + message + "<")
#	if message.startswith("USDT") == True:
#		message.replace("USDT ", "")
#		print("Setting USDT to: " + message)
		
bot.infinity_polling()
