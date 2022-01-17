#!/usr/local/bin/python3.10
# Modify the previous line with your own python settings

# BITBOT - Open Source Crypto Bot Trading Binance Api Based
# Software Released as GPL 3
#
# If you want to contribute please contact me at oculus@oculus.it 
#
# DON'T USE THIS SOFTWARE WITH REAL CRYPTOS, IT IS IN PRE-PRE-PRE-ALPHA TESTING

import configparser
import requests
import time
import json
#import sys
#from pynput import keyboard
from datetime import datetime
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

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
 #print("\nclient.get_asset_balance(asset='USDT')")
 print("USDT AVAILABLE: " + str(client.get_asset_balance(asset=sfiat)['free']), end='')
 print(" - BTC  AVAILABLE: " + str(client.get_asset_balance(asset=scrypto)['free']), end='')
 print(" - BNB  AVAILABLE: " + str(client.get_asset_balance(asset="BNB")['free']))
 
def sell(q):
 tentativi = 0
 while True:
  try:
   print("Selling " + scrypto + " " + str(q))
   order = client.order_market_sell(symbol=symbol, quantity=q)
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
   return order
  except:
   print("Error Buying - Try #",end='')
   print(tentativi)
   time.sleep(1)
   tentativi +=1
   order = "Errore"
   if tentativi > 5:
    return order


def vendi():
  global venduto, totalebitacquistati, attuale, guadagno, comprato, guadagnototale, totalebitacquistati, numerobitacquistati, prezzomedio, media, up, down, compro, comprato, numeroacquisti
  print(colore.rosso + "\nS E L L I N G\n" + colore.reset)
#  q = round(float(totalebitacquistati),8)
  q = float(round(totalebitacquistati,6))
#  order = client.order_market_sell(symbol='BTCUSDT', quantity=q)
  if simulate == 0:
   esito = sell(q)
   if q == "Errore":
    print("Error during selling. Please, perform a manual check!!")
   else:
    #print(esito)
    attuale = float(esito["fills"][0]["price"])
  else:
    print("Simulation not available at the moment!")
    
  Saldo()
   
  #print(type(q))
  venduto = totalebitacquistati * attuale
  print(f"Selled at {sfiat} {attuale} and gained {venduto}")
  guadagno = venduto - comprato
  guadagnototale = guadagnototale + guadagno
  print(f"Actual Gain: {sfiat} {guadagno}  Total Gain: {sfiat} {guadagnototale}   -  ", end='')
  c = 100
  x = lambda a, b: (a * c / b) - c
  r = x(venduto, comprato)
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
  #print(f"\n\ntotalebitacquistati: {totalebitacquistati} - numeroacquisti: {numeroacquisti} - prezzomedio: {prezzomedio} - media: {media}")
  #print(f"up: {up} - down: {down} - compro: {compro} - comprato: {comprato}")
  if ferma == 1:
   quit()
   
  return True

def compra():
  global bitcoin, fiat, attuale, comprato, temporanea, numeroacquisti, totalebitacquistati, prezzomedio, up, down
  print(colore.verde + "\nB U Y\n" + colore.reset)
  bitcoin = fiat / attuale
  #print(bitcoin)
  #q=round(float(bitcoin),8)
  q = float(round(bitcoin,6))
  #print("Buying " + scrypto, end='')
  #print(q)
  #print(type(q))
  #order = client.order_market_buy(symbol='BTCUSDT', quantity=q)
  print("Values before buying: ", end='')
  Saldo()
  if simulate == 0:
   esito = buy(q)
   if esito == "Errore":
    print("Error during buying. Please perform a manual check!!")
   else:
    #print(esito)
    attuale = float(esito["fills"][0]["price"])
    bitcoin = float(esito["fills"][0]["qty"])
    if bitcoin * attuale < fiat:
      print("Now buying %.8f at price of %.2f and the total is %.2f but is less than %.2f" %(bitcoin, attuale, bitcoin * attuale, fiat))
      if debug == 1:
       print(esito)
  else:
   print("Simulation not available at the moment!")
   
  print("Values after buying:  ", end='')   
  Saldo()
  comprato = bitcoin * attuale + comprato
  temporanea = bitcoin * attuale
  numeroacquisti = numeroacquisti + 1
  totalebitacquistati = totalebitacquistati + bitcoin
  prezzomedio = prezzomedio + attuale
  print(f"{colore.reset}", end='')
  print("\nB - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL CRYPTO VALUE: %.2f  " %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, attuale))
#  print(f"Comprato a € {attuale} per un valore di {temporanea}")
  up = 0
  down = 0
  return True
  
def LeggiConfig(modo):
 global api, sek, fiat, maxfiat, limite, pausa, ferma, nonvendo, configfile, testneturl
 config = configparser.ConfigParser()
 config.read_file(open(r''+configfile))
 if modo == 1:
  api = config.get('binance', 'api')
  sek = config.get('binance', 'sek')
  testneturl = config.get('binance', 'testneturl')
  maxnonvendo = int(config.get('Var', 'maxsell'))
  debug = int(config.get('Var', 'debug'))
 if modo == 2:
  fiat = int(config.get('Var', 'fiat'))
  ferma = int(config.get('Var', 'stop'))
  maxfiat = int(config.get('Var', 'maxfiat'))
  #limite = int(config.get('Var', 'limit'))
  pausa = int(config.get('Var', 'pause'))
  debug = int(config.get('Var', 'debug'))
 if modo == 3:
  fiat = int(config.get('Var', 'fiat'))
  ferma = int(config.get('Var', 'stop'))
  maxfiat = int(config.get('Var', 'maxfiat'))
  limite = int(config.get('Var', 'limit'))
  pausa = int(config.get('Var', 'pause'))
  maxnonvendo = int(config.get('Var', 'maxsell'))
  debug = int(config.get('Var', 'debug'))

rel = "0.7 binance trading test"

scrypto = "BTC"
sfiat   = "USDT"
symbol  = scrypto + sfiat

configfile = "/etc/bitbot/"+symbol+".config"
 
LeggiConfig(1)

# Edit api and sek variables with your BINANCE TESTING APIs
#api = ''
#sek = ''

# To use the real BINANCE API TRADING change testnet to zero
# DURING THE TEST PLEASE DON'T USE REAL BINANCE API TRADING WITH REAL CRYPTOS.
testnet = 1

# Perform SIMULATIONS only
# If simulate = 1 the BOT will not trade any crypto. If simulate = 0 the BOT will trade cryptos in test o real mode.
simulate = 0
# SIMULATIONS NOT AVAILABLE AT THIS MOMENT

try:
 client = Client(api, sek)
 if testnet == 1:
  client.API_URL = testneturl 
  #'https://testnet.binance.vision/api'
except:
 print("ERROR: Cannot connect to Binance APIs. Check your internet connection and your keys activation.")
 quit()

try:
 client.get_account()
except:
 print("ERROR: Cannot connect to Binance APIs. Check your internet connection and your keys activation.")
 quit()

class colore:
  verde = '\033[92m'
  rosso = '\033[91m'
  giall = '\033[93m'
  reset = '\033[0m'
 
        
print(colore.verde + "\n\nBBBBBBB   II  TTTTTTTT   BBBBBBB     OOOOO   TTTTTTTT")
print("BB    BB  II     TT      BB    BB   OO   OO     TT")
print("BBBBBBB   II     TT      BBBBBBB   OO     OO    TT")
print("BB    BB  II     TT      BB    BB  OO     OO    TT")
print("BB     BB II     TT      BB     BB OO     OO    TT")
print("BB    BB  II     TT      BB    BB   OO   OO     TT")
print("BBBBBBB   II     TT      BBBBBBB     OOOOO      TT          C R Y P T O - A U T O T R A D E R ")
print("                                                                       by Oculus.it" + colore.reset)
print("")


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
debug = 0						  # Enable (1) or disable (0) debug messages


print(colore.giall + "Rel " + rel + " - "+ symbol + " by Oculus.it\n\n" + colore.reset)


#with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#  print("Premi M per MENU")
while True:
   
  
  while number < maxloop:
    LeggiConfig(2)
    
    if ferma == 1:
      print(colore.reset + "Stop at first crypto selling with gain!")
  
  
    try:
      #print(symbol)
      response = client.get_symbol_ticker(symbol=symbol)
      #response = client.get_asset_balance(asset='BTC')
      #print(response['price'])
      attuale = float(response['price'])
      valoreattuale = totalebitacquistati * attuale
    except:
      print(colore.reset + "Connection error!")
    
    if numeroacquisti > 0:
      media = prezzomedio / numeroacquisti
      
    now = datetime.now()    
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
      
      
    if precedente == attuale:
      print(f"{colore.giall}", end='')
      print("\n= - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))

    if precedente < attuale:
      up = up + 1
      if up == 2:
        down = 0 

      print(f"{colore.verde}", end='')
      print("\n^ - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))
    
    if precedente > attuale:
      down = down + 1
      if down == 2:
        up = 0
      print(f"{colore.rosso}", end='')
      print("\nv - %s - UP: %.0f  DOWN: %.0f  LG: %.2f  TG: %.2f  TOTAL CRYPTO BOUGHT: %.8f  \nTOTAL VALUE BOUGHT: %.2f  ACTUAL VALUE: %.2f  ACTUAL CRYPTO VALUE: %.2f  AVERAGE: %.2f" %(dt_string, up, down, guadagno, guadagnototale, totalebitacquistati, comprato, valoreattuale, attuale, media))

    if comprato > 0:
     actualgain = 100 - ((valoreattuale*100)/comprato)
     print("\nActual Gain: {actualgain} %")
    else:
     actualgain = 0
    
    if actualgain > 0.05:
        vendi()
        compra()
        
    if actualgain < 0.1:
        compra()
        
    if up > limite:                                               # Controlla se il numero di UP supera il LIMITE impostato
      if down > 0:                                                # Controlla che ci sia stato almeno un DOWN ad indicare che il mercato era salito ed ora scende 
        if comprato > 0:                                          # Controlla che siano stati comprate crypto
          if numeroacquisti > 0:                                  # Check if numeroacquisti is 
            confronto = prezzomedio / numeroacquisti
            print("DEBUG!! " + str(confronto-attuale))
            if attuale > confronto:
              vendi()
              compra()
            else:
              print(f"\nI cannot sell now because {scrypto} is actually: {attuale}  lower than the Average Buy of {scrypto}: {confronto}\n")
              nonvendo = nonvendo + 1
              if nonvendo > maxnonvendo:
                limite = limite - 1
                if limite < 1:
                  limite = 1
                print(colore.reset + "I lower the gain/loss limit at " + str(limite))
        else:
          print(colore.reset + "\nThere are no crypto to sell\n")
          compro = compro + 1
        #up = 0
        #down = 0
        
    if down > limite:
      if up > 0:
        #print(colore.verde + "\nB U Y\n" + colore.reset)
        if comprato > 0:
          if comprato >= maxfiat:
            print(colore.rosso + f"No {sfiat} available to buy cryptos!" + colore.reset)
          else:
            compra()
            print(f"Bought {scrypto} at {sfiat} {attuale} - Total value {temporanea}")
        else:
          compra()
          print(f"Bought {scrypto} at {sfiat} {attuale} - Total value {comprato}")
        up = 0
        down = 0  

    if number == 0:
      compro = limite + 1
            
    if compro > limite:
      if number == 0:
        print(colore.verde+ "\nStarting buying some crypto! B U Y!!\n" + colore.reset)
      else:
        print(colore.verde + "\nMarket is good now, B U Y!!\n" + colore.reset)

      compra()        
      compro = 0
      #up = 0
      #down = 0
      #prezzomedio = prezzomedio + attuale
    
    time.sleep(pausa)
    number = number + 1
    precedente = attuale  
    
#    listener.join()
