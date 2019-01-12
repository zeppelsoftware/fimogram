#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@uthor b3zi / lucamayer
#telegram: @zeppel
#github.com/zeppelsoftware/fimogram
#!Linux base application
#setup
import sys
from subprocess import call

def main():
	print "fimogram by zeppel"
	print "github.com/zeppelsoftware/fimogram"
	print "-------------------------"
	print "creating fimo.config"
	print "Telegram ID: "+sys.argv[1]
	print "Telegrambot token: "+sys.argv[2]
	file = open("fimo.config","w") 
	file.write("telegramID="+sys.argv[1]+"\n") 
	file.write("botToken="+sys.argv[2]) 
	file.close()
	print "install python-telegram-bot API"
	call(["pip", "install", "python-telegram-bot", "--upgrade"])
	print "install overlook-fing-3.0"
	call(["dpkg", "-i", "fing.deb"])
if __name__=="__main__":
   main();
