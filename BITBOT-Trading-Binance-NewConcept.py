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
#import sys
#from pynput import keyboard
from datetime import datetime
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager


######## RELEASE VERSION ##############################################
rel = "0.9.016 Binance Trading ** TEST NEW CONCEPT & TELEGRAM INTEGRATION **"

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
  black='\033[30m'
  red='\033[31m'
  green='\033[32m'
  orange='\033[33m'
  blue='\033[34m'
  purple='\033[35m'
  cyan='\033[36m'
  lightgrey='\033[37m'
  darkgrey='\033[90m'
  lightred='\033[91m'
  lightgreen='\033[92m'
  yellow='\033[93m'
  lightblue='\033[94m'
  pink='\033[95m'
  lightcyan='\033[96m'

def notify(bot_message):
 global telegramtoken, telegramchatid
 bot_token = telegramtoken
 bot_chatID = telegramchatid
 send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
 #print(send_text + "\n" + telegramtoken)
 try:
  response = requests.get(send_text)
  if debugge == 1:
   print(colore.verde + "-----> Telegram Notify Sended <-----" + colore.reset)
 except:
  if debugge == 1:
   print(colore.rosso + "-----> Telegram Notify Error <-----" + colore.reset)
 return response.json()

def on_press(key):
  tasto = key
#  try:
    #print('Tasto {0}', format(key.char))
#  except AttributeError:
    #print('Speciale {0}'. format(key))
    
def on_release(key):
  print(key)
  tasto = format(key)
#  print(tasto)
  if tasto == "'m'":
    print('Menu:')
    print('Q - Quit')
    return True
  if tasto == "'q'":
    print('Termino il programma tra pochi secondi')
    number = maxloop + 1
    return True
    
def Saldo():
 global sfiat, scrypto
 # get balance for a specific asset only (BTC)
 print("USDT AVAILABLE: " + str(client.get_asset_balance(asset=sfiat)['free']), end='')
 print(f" - {scrypto}  AVAILABLE: " + str(client.get_asset_balance(asset=scrypto)['free']), end='')
 print(" - BNB  AVAILABLE: " + str(client.get_asset_balance(asset="BNB")['free']))
 
def sell(q):
 tentativi = 0
 while True:
  try:
   print("Selling " + scrypto + " " + str(q))
   order = client.order_market_sell(symbol=symbol, quantity=q)
   print(order["status"])
   return order
  except:
   print("Error Selling - Try #",end='')
   print(tentativi)
   time.sleep(1)
   tentativi +=1
   order = "Errore"
   if tentativi > 5:
    return order

def buy(q):
 tentativi = 0
 while True:
  print("Buying " + scrypto + " " + str(q))
  try:
   order = client.order_market_buy(symbol=symbol, quantity=q)
   esitooperazione = order["status"]
  except:
   esitooperazione = "ERROR"  
  finally:
    if esitooperazione == "FILLED":
     return order
    if esitooperazione == "ERROR":
     print("Error Buying - Try #",end='')
     print(tentativi)
     time.sleep(1)
     tentativi +=1
     order = "Errore"
     if tentativi > 5:
      return order
    else:
     return order



def vendi():
  global dt_string, venduto, totalebitacquistati, attuale, guadagno, comprato, guadagnototale, totalebitacquistati, numerobitacquistati, prezzomedio, media, up, down, compro, comprato, numeroacquisti, valoreattuale, losspc, gainpc, media, location
  print(colore.rosso + "\nS E L L I N G\n" + colore.reset)

  q = float(round(totalebitacquistati,6))
  if simulate == 0:
   esito = sell(q)
   if q == "Errore":
    print("Error during selling. Please, perform a manual check!!")
   else:
    try:
     attuale = float(esito["fills"][0]["price"])
    except:
     print(colore.lightred + "Error selling " + str(q) + " " + scrypto + ". Please check it!! A notification was sent to telegram account" + colore.reset)
     notify("BITBOT " + location + " - Error selling " + str(q) + " " + scrypto + ". Please check it!! Script will be ended now.")
     quit(1)
  else:
    print("Simulation not available at the moment!")
    
  Saldo()
  log = open(symbol + ".log","a")
  log.write("EXPECT;" + dt_string + ";Crypto Qty: " + str(q) + ";Actual Crypto Value: " + str(attuale) + ";Total: " + str(q * attuale) + ";Gain %: " + str(gainpc) +";Loss %: " + str(losspc) +";0\n") 
  venduto = totalebitacquistati * attuale
  print(f"Selled at {sfiat} {attuale} and gained {venduto}")
  
  guadagno = venduto - comprato
  guadagnototale = guadagnototale + guadagno
  print(f"Actual Gain: {sfiat} {guadagno}  Total Gain: {sfiat} {guadagnototale}   -  ", end='')
  telegram_message = "BITBOT " + location + " - " + dt_string + " - Selled " + str(q) + " " + scrypto + " at actual value of " + str(attuale) + " " + sfiat + "\n\n- Actual Gain: " + str(guadagno) + "\n- Total Gain: " + str(guadagnototale)
  notify(telegram_message)

  c = 100
  x = lambda a, b: (a * c / b) - c
  r = x(venduto, comprato)
  
  log.write("SELL;" + dt_string + ";" + str(q) + ";" + str(attuale) + ";" + str(q * attuale) + ";" + str(venduto) + ";" + str(guadagno) + ";" + str(guadagnototale) + "\n")
  log.close
  if os.path.exists(symbol + ".sav"):
   os.remove(symbol + ".sav")
  else:
   print("The file " + symbol + ".sav does not exist") 
   
  #sav = open(symbol + ".sav", "w")
  #sav.write("[saving]\n")
  #sav.write("guadagno = 0\n")
  #sav.write("guadagnototale = 0\n")
  #sav.write("totalebitacquistati = 0\n")
  #sav.write("comprato = 0\n")
  #sav.write("media = 0\n")
  #sav.write("prezzomedio = 0\n")
  #sav.write("numeroacquisti = 0\n")
  #sav.write("gainav = 0\n")
  #sav.write("lossav = 0\n")  
  #sav.write("gainpc = 0\n")
  #sav.write("losspc = 0\n")
  #sav.write("gaincn = 0\n")
  #sav.write("losscn = 0\n")  
  #sav.write("gainsm = 0\n")
  #sav.write("losssm = 0\n")
  #sav.close
  print("%.4f" %(r), end='')
  print("%")
  print(f"\nResetting counters")
  totalebitacquistati = 0
  numeroacquisti = 0
  prezzomedio = 0
  media = 0
  up = 0
  down = 0
  compro = 0
  comprato = 0
  if ferma == 1:
   time.sleep(1)
   notify("BITBOT " + location + " - " + dt_string + " - STOPPED NOW by configuration settings.")
   quit(1)
   
  return True

def compra():
  global dt_string, bitcoin, fiat, attuale, comprato, temporanea, numeroacquisti, totalebitacquistati, prezzomedio, up, down, guadagnototale, valoreattuale, guadagno, media
  print(colore.verde + "\nB U Y\n" + colore.reset)
  
  bitcoin = fiat / attuale
  q = float(round(bitcoin,6))
  print("Values before buying: ", end='')
  Saldo()
  if simulate == 0:                                                      # Se NON è attiva la sola simulazione
   esito = buy(q)
   if esito == "Errore":
    print("Error during buying. Please perform a manual check!!")
   else:
    try:
     attuale = float(esito["fills"][0]["price"])
     bitcoin = float(esito["fills"][0]["qty"])
     if bitcoin * attuale < fiat:
      print("Now buying %.8f at price of %.2f and the total is %.2f but is less than %.2f" %(bitcoin, attuale, bitcoin * attuale, fiat))
      if debugge == 1:
       print(colore.rosso + "DEBUG: " + esito + colore.reset)
    except:
     print(colore.lightred + "-----> TRANSACTION ERROR <-----" + colore.reset)
     print(colore.rosso + esito + colore.reset)
  else:                                                                  # Altrimenti se la simulazione FOSSE ATTIVA
   print("Simulation not available at the moment!")
   
  print("Values after buying:  ", end='')   
  Saldo()
  comprato = (bitcoin * attuale) + comprato
  temporanea = bitcoin * attuale
  valoreattuale = comprato
  numeroacquisti = numeroacquisti + 1
  totalebitacquistati = totalebitacquistati + bitcoin
  prezzomedio = prezzomedio + attuale
  telegram_message = "BITBOT " + location + " - " + dt_string + " - Buyed " + str(q) + " " + scrypto + " at actual value of " + str(attuale) + " " + sfiat
  notify(telegram_message)

  sav = open(symbol + ".sav", "w")
  sav.write("[saving]\n")
  sav.write("guadagno = " + str(guadagno) + "\n")
  sav.write("guadagnototale = " + str(guadagnototale) + "\n")
  sav.write("totalebitacquistati = " + str(totalebitacquistati) + "\n")
  sav.write("comprato = " + str(comprato) + "\n")
  sav.write("media = " + str(media) + "\n")
  sav.write("prezzomedio = " + str(prezzomedio) + "\n")
  sav.write("numeroacquisti = " + str(numeroacquisti) + "\n")
  sav.write("gainav = " + str(gainav) + "\n")
  sav.write("lossav = " + str(lossav) + "\n")  
  sav.write("gainpc = " + str(gainpc) + "\n")
  sav.write("losspc = " + str(losspc) + "\n")
  sav.write("gaincn = " + str(gaincn) + "\n")
  sav.write("losscn = " + str(losscn) + "\n")  
  sav.write("gainsm = " + str(gainsm) + "\n")
  sav.write("losssm = " + str(losssm) + "\n")
  sav.close
  log = open(symbol + ".log","a")
  log.write("BUY;" + dt_string + ";" + str(bitcoin) + ";" + str(attuale) + ";" + str(bitcoin * attuale) + ";" + str(comprato) + ";" + str(valoreattuale) + ";0\n")
  log.close
  print(f"{colore.reset}", end='')
  print("\nB - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL CRYPTO VALUE: %.2f  " %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, attuale))
  up = 0
  down = 0
  return True
  
def LeggiSaving():
 global guadagno, guadagnototale, totalebitacquistati, comprato, media, symbol, gainav, lossav, gainpc, losspc, gaincn, losscn, gainsm, losssm, prezzomedio, numeroacquisti
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

 return True
 
def LeggiConfig(modo):
 global api, sek, fiat, maxfiat, limite, pausa, ferma, nonvendo, configfile, testneturl, gainpc, losspc, debugge, maxnonvendo, telegramtoken, telegramchatid, location
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
 if modo == 2:
  fiat = int(config.get('Var', 'fiat'))
  ferma = int(config.get('Var', 'stop'))
  maxfiat = int(config.get('Var', 'maxfiat'))
  pausa = int(config.get('Var', 'pause'))
  debugge = int(config.get('Var', 'debug'))
  mingain = float(config.get('Var', 'mingain'))
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
 if modo == 4:
  losspc = float(config.get('Var', 'losspc'))  

def variables():
 global numeroacquisti, totalebitacquistati, prezzomedio, comprato, guadagnototale, guadagno, compro, fiat, maxfiat, maxloop, limite, up, down
 global pausa, precedente, attuale, number, media, nonvendo, maxnonvendo, ferma, debugge, gainpc, losspc, gainsm, losssm, gainav, lossav
 global gaincn, losscn, actualgain, mingain, telegramtoken, telegramchatid, location
 ######## DEFINING VARIABLES ###########################################
 numeroacquisti = 0                # How many buying to calcolate the average
 totalebitacquistati = 0           # Total crypto bought
 prezzomedio = 0                   # Crypto average value
 comprato = 0                      #
 guadagnototale = 0                # Total gained
 guadagno = 0                      # Actual gain
 compro = 0                        #
 fiat = 500                        # Amount of Stable Coin to buy
 maxfiat = 2500                    # Max Stable Coins to buy
 maxloop = 1000000                 # Number of checks
 limite = 3                        # Limit of ups or downs to sell or buy
 up = 0                            # Current ups
 down = 0                          # Current downs
 pausa = 120                       # Pause between price checks
 precedente = 0                    # Previous
 attuale = 0                       # Actual
 number = 0                        #
 media = 0                         # Average
 nonvendo = 0                      # Numero di tentativi falliti nella vendita per media troppo bassa
 maxnonvendo = 3                   # Numero massimo di tentativi falliti prima di abbassare il numero LIMITE che non deve scendere sotto a: 1
 ferma = 0                         # Ferma il BOT TRADING alla prima vendita disponibile 1=STOP 0=NON STOP
 debugge = 0						              # Eable (1) or disable (0) debug messages
 gainpc = 0                        # Gain %
 losspc = 0                        # Loss %
 gainsm = 0                        # Gain Sum for Average computing
 losssm = 0                        # Loss Sum for Average computing
 gainav = 0                        # Gain Average
 lossav = 0                        # Loss Average
 gaincn = 0                        # Gain Counter
 losscn = 0                        # Loss Counter
 actualgain = 0                    # Actual gain
 mingain = 0.1					  # Minimum gain percentage
 telegramtoken = ''
 telegramchatid = ''
 location = ''

 
LeggiConfig(1)

######## TESTNET ######################################################
# To use the real BINANCE API TRADING change testnet to zero
# DURING THE TEST PLEASE DON'T USE REAL BINANCE API TRADING WITH REAL
# CRYPTOS.
#######################################################################
testnet = 1

######## SIMULATION ###################################################
# Perform SIMULATIONS only
# If simulate = 1 the BOT will not trade any crypto. 
# If simulate = 0 the BOT will trade cryptos in test o real mode.
#######################################################################
simulate = 0
######## SIMULATIONS NOT AVAILABLE AT THIS MOMENT #####################

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


 

######## STARTING THE BITBOT TRADING PROGRAM ##########################
print(colore.verde) 
print(" _______    ___   _______   _______    _______   _______   ")
print("|   _   \  |   | |       | |   _   \  |   _   | |       |  ")
print("|.  1   /  |.  | |.|   | | |.  1   /  |.  |   | |.|   | |  ")
print("|.  _   \  |.  | `-|.  |-' |.  _   \  |.  |   | `-|.  |-'  ")
print("|:  1    \ |:  |   |:  |   |:  1    \ |:  1   |   |:  |    ")
print("|::.. .  / |::.|   |::.|   |::.. .  / |::.. . |   |::.|    ")
print("`-------'  `---'   `---'   `-------'  `-------'   `---'    ")
print("            C R Y P T O - A U T O T R A D E R              ")
print("                       by Oculus.it                        ")
print(colore.reset + "\n")
print("")

variables()

######## READ CONFIGURATION MODE 3 AND SET GAIN AND LOSS AVERAGES #####
LeggiConfig(3)
gainav = gainpc
lossav = losspc
test = notify("BOT STARTED - Located in " + location)
#print(test)
print(colore.giall + "Rel " + rel + " - "+ symbol + " by Oculus.it\n\n" + colore.reset)

try:
 LeggiSaving()
 print(colore.lightcyan + "Restoring previous situation" + colore.reset)
 if debugge == 1:
  print(f"LG: {guadagno} - TG: {guadagnototale} - TOTAL CRYPTO BOUGHT: {totalebitacquistati} \nTOTAL VALUE BOUGHT: {comprato} - AVERAGE: {media}")
  print(f"AVERAGE SUM: {prezzomedio} - NUMBER OF BUYS: {numeroacquisti}")
  print(f"GAINAV: {gainav} - LOSSAV: {lossav} - GAINPC: {gainpc} - LOSSPC: {losspc}")
  print(f"GAINCN: {gaincn} - LOSSCN: {losscn} - GAINSM: {gainsm} - LOSSSM: {losssm}")
except:
  print(colore.lightcyan + "No restoring file found" + colore.reset)

#with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#  print("Premi M per MENU")
while True:                        # MAIN LOOP
  number = 0                       # RESTART WITH LOOPS
  while number < maxloop:          # COUNT MAX LOOP DEPRECATED
    LeggiConfig(2)
    print(colore.pink + "--------------------========== CHECKING CRYPTO VALUE ==========--------------------" + colore.reset)
    
    ######## CHECK IF THE BOT STOPS AT FIRST SELL #####################    
    if ferma == 1:
      print(colore.lightgrey + "Stop at first crypto selling with gain!" + colore.reset)

    ######## CHECK THE PRICE OF THE CRYPTO ############################
    try:
      response = client.get_symbol_ticker(symbol=symbol)
      attuale = float(response['price'])
      valoreattuale = totalebitacquistati * attuale
    except:
      print(colore.reset + "Connection error!")
    
    ######## CALCULATE AVERAGE PRICE ##################################
    if numeroacquisti > 0:
      media = prezzomedio / numeroacquisti
      
    now = datetime.now()    
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    # Inizio ad elaborare i dati e calcolo il guadagno % attuale
    #   Se il guadagno sarà maggiore di "gainpc" venderò e comprerò di nuovo
    #   Se il guadagno sarà minore di   "losspc" acquisterò ancora per mediare il prezzo

    if comprato > 0:                                      # if there are crypto bought then...
     actualgain = ((valoreattuale*100)/comprato) - 100
     print(f"{colore.giall}- ACTUAL +G/-L: ", end='')
     if actualgain < 0:
      print(colore.rosso, end='')
     if actualgain == 0:
      print(colore.giall, end='')
     if actualgain > 0:
      print(colore.verde, end='')
     
     print(f"{actualgain} % {colore.giall}")
    else:
     actualgain = 0
     compra()
          

    if actualgain > 0:
     gainsm = gainsm + actualgain
     gaincn = gaincn + 1
     gainav = gainsm / gaincn
     if gainav < mingain:
       gainav = mingain
		 
    if actualgain < 0:
     losssm = losssm + actualgain
     losscn = losscn + 1
     lossav = losssm / losscn      

    if debugge == 1:
      print("Controllo se posso vendere:")
    if actualgain > gainpc:
      vendi()
      compra()
      print(colore.lightred)
      gainav = gainsm / gaincn
      print(f"==========> Changing GAIN % to {gainav}")
      lossav = losssm / losscn
      print(f"==========> Changing LOSS % to {lossav}")
      print(colore.reset)
    else:
      if debugge == 1:
        print(f"actualgain {actualgain} - gainpc {gainpc}")

    if actualgain < losspc:
     if comprato + fiat > maxfiat:
      print(colore.lightred)
      print(f"- Max {sfiat} reached.")
      print(colore.reset)
     else:
      compra()
      LeggiConfig(4)
      #### DA CONTROLLARE CHE FUNZIONI ####
      # If LossAverage is < than Loss%Limit the Loss%Limit is decreased to avoid continuous buying
      
      print(f"actualgain: {actualgain} - losspc: {losspc} - lossav: {lossav}")
      losspc = lossav + losspc   #prima era un -
      print(colore.lightgrey + "Loss % is decreased to avoid continuous buying to " + str(losspc) + "%" + colore.reset)

        
    print(f"{colore.giall}- GAIN AVERAGE: {colore.verde}{gainav}%")
    print(f"{colore.giall}- LOSS AVERAGE: {colore.rosso}{lossav}%")
    print(f"{colore.giall}- GAIN LIMIT  : {colore.verde}{gainpc}%")
    print(f"{colore.giall}- LOSS LIMIT  : {colore.rosso}{losspc}%" + colore.reset)
      
      
    # Stampo a video le variazioni attuali  
    if precedente == attuale:                      # I valori delle crypto sono uguali
      print(f"{colore.giall}", end='')
      print("\n= - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))

    if precedente < attuale:                       # Se attualmente la crypto è maggiore del precedente
      up = up + 1
      if up == 2:
        down = 0 

      print(f"{colore.verde}", end='')             
      print("\n^ - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))
    
    if precedente > attuale:                       # Se attualmente la crypto è minore del precedente
      down = down + 1
      if down == 2:
        up = 0
      print(f"{colore.rosso}", end='')
      print("\nv - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))

    
    if debugge == 1:
      print(f"DEBUG: UP {up} - DOWN {down} - LIMIT {limite} - GAINAV {gainav} - LOSSAV {lossav}")
    
    if up > limite and gainav > 0:	
      gainpc = gainav
      print(f"{colore.lightgreen}==========> Changing GAIN % to {gainav} {colore.reset}")
      up = 0
      down = 0
      
    if down > limite and lossav < 0:
      losspc = lossav
      print(f"{colore.lightred}==========> Changing LOSS % to {lossav} {colore.reset}")
      down = 0
      up = 0
    
    print(colore.pink + "--------------------==========#######################==========--------------------\n" + colore.reset)
    # Pause, increase counter and swap the previous crypto value with the actual one    
    time.sleep(pausa)
    number = number + 1
    precedente = attuale  
    
#    listener.join()
