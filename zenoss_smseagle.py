#! /usr/bin/env python
# ============================== SUMMARY =====================================
#
# Program : zenoss_smseagle.py
# Version : 1.0
# Date : May 13 2013
# Author : SMSEagle Team
# Summary : This plugin sends ZenOss SMS alerts with SMSEagle hardware sms gateway
# Copyright (c) 2013, SMSEagle www.smseagle.eu
# License : BSD
#
# ============================= MORE INFO ======================================
#
# Visit: http://www.smseagle.eu
# The latest version of this plugin can be found on:
# http://bitbucket.org/proximus/smseagle-zenoss
#
# ============================== SETUP =========================================
#
# 1. Create a user in SMSEagle and assign to it the right permissions
#
# 2. Edit variables SMSEAGLE_TOKEN, SMSEAGLE_IP, SMSEAGLE_TYPE in code below
#
# 3. Configure Zenoss (see tutorial http://www.smseagle.eu/plugins.php)
#
# ==============================================================================
# If logs are enabled they are saved to $ZENHOME/log/sms_smseagle.log
# where $ZENHOME is your Zenoss directory


import os
import sys
import time
import requests

# Edit these settings to match your own
SMSEAGLE_TOKEN = "123abc456def"
SMSEAGLE_IP = "192.168.0.101"
SMSEAGLE_TYPE = "sms"
SMSEAGLE_DURATION = 10
SMSEAGLE_VOICE_ID = 1
LOG_ENABLED = 0
#

def main():

    try:
       	# Read recipient number
        rcpt = sys.argv[1]
    except:
        print("Invalid arguments! Usage: zenoss_smseagle <recipient>")
        sys.exit(1)
    
    try:
	# Open logfile if logging enabled
       	if LOG_ENABLED:
            file = os.environ['ZENHOME']+"/log/sms_smseagle.log"
            log = open(file, 'a')
    except:
        print("Cannot open log file!")
        sys.exit(2) 
    	
    try:
        msg = ""
        
       	# Read message from standard in
       	if SMSEAGLE_TYPE != 'ring':
       	    msg = sys.stdin.read()
       	
       	method = "messages/sms"
       	
       	match (SMSEAGLE_TYPE):
       	    case 'ring':
       	        method = 'calls/ring'
            case 'tts':
                method = 'calls/tts'
            case 'tts_adv':
                method = 'calls/tts_advanced'

       	# Prepare HTTP request
       	url = "http://"+SMSEAGLE_IP+"/api/v2/"+method
       	query_args = {'to':[rcpt]}
       	
       	match (SMSEAGLE_TYPE):
            case 'ring':
                query_args['duration'] = SMSEAGLE_DURATION
            case 'tts':
                query_args['text'] = msg
                query_args['duration'] = SMSEAGLE_DURATION
            case 'tts_adv':
                query_args['text'] = msg
                query_args['duration'] = SMSEAGLE_DURATION
                query_args['voice_id'] = SMSEAGLE_VOICE_ID
            case _:
                query_args['text'] = msg
       	
       	# Write log if logging enabled
       	if LOG_ENABLED:
       	    timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
       	    log.write("%s ===== BEGIN SENDING SMS ==== \n" % timestamp)			
       	    log.write("%s SMS recipient: %s\n" % (timestamp, rcpt))
       	    if SMSEAGLE_TYPE != 'ring':
       	        log.write("%s SMS text: %s\n" % (timestamp, msg))
			
       	#HTTP request to SMSEagle
       	result = requests.post(url, json = query_args, headers={"Content-Type":"application/json", "access-token":SMSEAGLE_TOKEN})
       	print(result)
       	print(result.content.decode('UTF-8'))
    	
        # Write log if logging enabled
        if LOG_ENABLED:
            timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
            try:
                log.write("%s Sending result: %s\n%s" % (timestamp, result, result.content.decode('UTF-8')))
                log.write("%s ===== END SENDING SMS ====\n" % timestamp)
            finally:
                log.close()
    except Exception as e:
        print(e)
        sys.exit(1)
		
    
main()
