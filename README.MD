# ***BITBOT - Trading BOT Binance API Powered***

This is a *pre-release* actually in **TESTING RELEASE**. This is an unstable release.
Use only with TESTING BINANCE API. 
Do not use with your real crypto. 

### You can lost all of your cryptos using this **UNSTABLE TESTING RELEASE.**
> I'm not responsible of yout cryptos and money!
>> **USE ONLY IF YOU UNDERSTAND IT.** ***NOT TESTED ON REAL BINANCE ACCOUNT***.

## HOW TO START
- Download and compile Python 3 or install it from your distro's repository
- Configure the first line of BITBOT-Trading-Binance.py with your Python settings. Minimun Python 3 required.
- Install requirements with *"pip install"* command
- Configure api & key varables with yours from **BINANCE TESTING API MODE**

## Compiling Python 3.10.x
- Download sources from **python.org**
- Decompress in a folder and, with the terminal, enter in the folder Python-3.10.x (where x is sub version if present)
- Check system configuration with *./configure --enable-optimizations*
- Compile with *make* command and ***take a coffee***, a ***beer*** or better a ***japanese green tea***. If your PC is very slow you can have your japanese green tea in Japan!
- Install with *sudo make install* command
- You'll find your Python 3 installation in /usr/local/bin 

## Configuring BITBOT
In order to start the *BITBOT* software you have to create a folder in your **/etc** directory named ***bitbot*** and create a file named with your ***Crypto-PAIR.config***.
For example, if you need to operate on the BTC/USDT pair, you need to create the file **/etc/bitbot/BTCUSDT.config**.

You can start from the *BITBOT.ini* file that you can find in this repository.

The content is:
>[binance]
>api = 
>sek = 
>testneturl = 
>
>[Var]
>fiat = 25
>maxfiat = 2500
>limite = 3
>pausa = 120
>ferma = 0
>maxnonvendo = 0

In the *[binance]* block you have to place the API (api) and the Secret (sek) passphrase that you can find, or create, in your *Binance API Section*.
The *testneturl* can be blank if you operate on the official *Trading API* or you can fill with the testnet URL ***https://testnet.binance.vision/api***.

In the *[Var]* block you can specify the **BOT RULES**:
- *fiat* is the amount of *stable coin* to buy each time the bot want to buy a crypto asset.
- *maxfiat* is the maximum amount of *stable coin* that the bot can use.
- *limite*  is the maximum number of times that the crypto gain or loss.
- *pausa* is the time between a price check and another
. *ferma* is 0 if the bot will allways operate. If *ferma* is 1 the bot will stop operating at next gain and selling of cryptos.
. *maxnonvendo* ...

For each *BOT* you can copy a script with the name of the crypto pair. So you can run more than one *BOT* simultaneously.

