# FIMOGRAM
### FiMoGram - A Telegram home network monitoring bot

## What is it?
fimogram is made for home network monitoring. It is combined with Telegram so you can easy access your home network from all over the world without an additional app.

## Installation

1. `git clone https://github.com/zeppelsoftware/fimogram.git`
2. `sudo python setup.py <your TelegramID> <your TelegramBotToken>`
    1. For TelegramID message [@getchat_idbot](http://t.me/getchat_idbot)
    2. For BotToken message [@BotFather](http://t.me/botfather)
3. `sudo python fimogram.py`

## Documentation

cmd|description
------------ | -------------
/help | show help
/start | start bot
/sscan | simple network scan
/ascan | advanced network scan
/fscan | full network scan
/check [hostname/WebURL/IP] | check if device/website is online
