#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@uthor b3zi / lucamayer
#telegram: @lucamayer
#github.com/b3zi/fimogram

#!Linux base application

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from subprocess import call
import os

telegramID = 344927076
BotToken = '523012190:AAH5LC7unWIN4k9qMbc2IIPRGLdZKXj7ag4'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
	update.message.reply_text('Whatup :D networkmonitoring bot by b3zi (C) github.com/b3zi/fimogram ')
	
def update(bot, update):
	update.message.reply_text("Checking for online devices...")
	call(["fing", "-r", "1", "-o", "log,csv,fing.log"]) # we update the fing.log
	file = open('fing.log', 'r') # open log 
	data=[x.split(';') for x in file.read().split('\n')]
	i=0
	outer = []
	while i<len(data)-1:
		out =  data[i][4].replace(".fritz.box", "") #speacial fo fritz box for nice display.
		#out =  data[i][4] # use this one if you are NOT using a fritz.box
		outer.append(out)
		i+=1
	message = '\n'.join(outer)
	bot.sendMessage(telegramID, message+'\n\n'+str(len(outer))+' devices online.')
	os.remove('fing.log') #clean up
def help(bot, update):
	update.message.reply_text('FIMOGRAM - b3zi will help you. Simply text @lucamayer')

def echo(bot, update):
	update.message.reply_text('Sorry, please use /help or check on github.com/b3zi/fimogram')
	
def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"', update, error)
	bot.sendMessage(telegramID, 'An error accured. Check your code.')


def main():
	updater = Updater(BotToken)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("scan", update))
	dp.add_handler(MessageHandler(Filters.text, echo))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
