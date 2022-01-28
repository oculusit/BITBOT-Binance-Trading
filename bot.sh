#!/bin/bash
while :
do
  ./BITBOT-Trading-Binance-NewConcept.py
  if [ $? -eq 1 ]
  then
   echo "Ended by AUTO STOP FUNCTION"
   break
  fi
done
echo "Ended by ERROR!!"
