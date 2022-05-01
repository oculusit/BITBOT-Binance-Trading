#!/bin/bash
while :
do
  echo "Verifying new releases from GITHUB..."
  wget https://raw.githubusercontent.com/oculusit/BITBOT-Binance-Trading/main/BITBOT-Trading-Binance-NewConcept.py --no-cache -O BITBOT.py
  chmod 755 BITBOT.py
  ./BITBOT.py
  echo "Errorlevel $?"
  if [ $? -eq 2 ]
  then
   echo "Ended by AUTO STOP FUNCTION - Errorlevel $?"
   echo "Verifying new releases of BASH from GITHUB..."
   wget https://raw.githubusercontent.com/oculusit/BITBOT-Binance-Trading/main/bot.sh --no-cache -O bot.sh
   chmod 755 bot.sh
   break
  else
   echo "Ended by Error!! Errorlevel $?"
  fi
done

