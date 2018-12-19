#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@uthor b3zi / lucamayer
#telegram: @zeppel
#github.com/b3zi/fimogram
#!Linux base application
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from subprocess import call
import os
#read config
config = [line.rstrip('\n') for line in open('fimo.config')]
telegramID = int(config[0].replace("telegramID=", ""))
botToken = str(config[1].replace("botToken=", ""))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def start(bot, update):
	starter = str(format(update.message.from_user['username']))
	userid = int(format(update.message.from_user['id']))
	print userid
	print telegramID
	update.message.reply_text('Whatup :D networkmonitoring bot by b3zi (C) github.com/b3zi/fimogram ')
	if userid != telegramID:
		update.message.reply_text('Hello '+starter+'. I am sorry, you are not the hoster of this bot. That is the reason why you are blocked from now on.')
		
def updateFing(update):
	update.message.reply_text("Checking for online devices...")
	call(["fing", "-r", "1", "-o", "log,csv,fing.log"]) # we update the fing.log
	file = open('fing.log', 'r') # open log 
	data=[x.split(';') for x in file.read().split('\n')]
	os.remove('fing.log') #clean up
	return data

	
def simplescan(bot, update):
	if int(format(update.message.from_user['id'])) != telegramID:
		#ignore
		print "unknown user"
	else:
		fingData = updateFing(update)
		i=0
		outer = []
		while i<len(fingData)-1:
			out =  fingData[i][4].replace(".fritz.box", "") #speacial fo fritz box for nice display.
			#out =  fingData[i][4] # use this one if you are NOT using a fritz.box
			outer.append(out)
			i+=1
		message = '\n'.join(outer)
		bot.sendMessage(telegramID, message+'\n\n'+str(len(outer))+' devices online.')
	
def advancedscan(bot, update):
	if int(format(update.message.from_user['id'])) != telegramID:
		#ignore
		print "unknown user"
	else:
		fingData = updateFing(update)
		i=0
		outer = []
		while i<len(fingData)-1:
			out =  fingData[i][4]+', '+fingData[i][2]+', '+fingData[i][6]
			outer.append(out)
			i+=1
		message = '\n'.join(outer)
		bot.sendMessage(telegramID, message+'\n\n'+str(len(outer))+' devices online.')

def fullscan(bot, update):
	if int(format(update.message.from_user['id'])) != telegramID:
		#ignore
		print "unknown user"
	else:
		fingData = updateFing(update)
		i=0
		outer = []
		while i<len(fingData)-1:
			out = fingData[i][2]+', '+fingData[i][4]+', '+fingData[i][5]+', '+fingData[i][6]
			outer.append(out)
			i+=1
		message = '\n'.join(outer)
		bot.sendMessage(telegramID, message+'\n\n'+str(len(outer))+' devices online.')

def isOnline(bot, update, args, job_queue, chat_data):
	if int(format(update.message.from_user['id'])) != telegramID:
		#ignore
		print "unknown user"
	else:
		device = args[0]
		#update.message.reply_text("Checking for "+device)
		call(["fing", "-p", device, "-o", "csv,"+device+".log"]) # we update the fing.log
		try:
			file = open(device+'.log', 'r') # open log 
			data=file.read()
			os.remove(device+'.log') #clean upif findWholeWord('0')(data):
			bot.sendMessage(telegramID, device+" is online.")
		except IOError:
			bot.sendMessage(telegramID, device+" is not available.")

def help(bot, update):
	update.message.reply_text('FIMOGRAM - github.com/b3zi/fimogram - Simply text @lucamayer for help')
	if int(format(update.message.from_user['id'])) != telegramID:
		#ignore
		print "unknown user"
	else:
		bot.sendMessage(telegramID, 'Available commands: \n/start - start bot\n/sscan - simple network scan\n/ascan - advanced network scan\n/fscan - full network scan\n/check [hostname/IP/WebURL] - Check if a device is online.')

def echo(bot, update):
	update.message.reply_text('Sorry, please use /help or check on github.com/b3zi/fimogram')
	
def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"', update, error)
	#bot.sendMessage(telegramID, 'An error accured. Check your code.')

def main():
	updater = Updater(botToken)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("sscan", simplescan))
	dp.add_handler(CommandHandler("ascan", advancedscan))
	dp.add_handler(CommandHandler("fscan", fullscan))
	dp.add_handler(CommandHandler("check", isOnline, pass_args=True, pass_job_queue=True, pass_chat_data=True))

	dp.add_handler(MessageHandler(Filters.text, echo))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
