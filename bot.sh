#!/bin/bash
while :
do
  ./BITBOT-Trading-Binance-NewConcept.py
  if [ $? -eq 1 ]
  then
   echo "Ended by AUTO STOP FUNCTION"
   break
  else
   echo "Ended by Error!! Errorlevel $?"
  fi
done

