#!/bin/bash
while :
do
  ./BITBOT-Trading-Binance-NewConcept.py
  echo "Errorlevel $?"
  if [ $? -eq 2 ]
  then
   echo "Ended by AUTO STOP FUNCTION - Errorlevel $?"
   break
  else
   echo "Ended by Error!! Errorlevel $?"
  fi
done

