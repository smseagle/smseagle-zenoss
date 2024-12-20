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
# 1. Create a user/password in SMSEagle
#
# 2. Edit variables SMSEAGLE_USER, SMSEAGLE_PASSWORD, SMSEAGLE_IP in code below
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
SMSEAGLE_DURATION = "10"
SMSEAGLE_VOICE_ID = "1"
LOG_ENABLED = 0
#

def main():

    try:
       	# Read recipient number
        rcpt = sys.argv[1]
    except:
        print "Invalid arguments! Usage: zenoss_smseagle <recipient>"
        sys.exit(1)
    
    try:
	# Open logfile if logging enabled
       	if LOG_ENABLED:
            file = os.environ['ZENHOME']+"/log/sms_smseagle.log"
            log = open(file, 'a')
    except:
        print "Cannot open log file!"
        sys.exit(2) 
    	
    try:
       	# Read message from standard in
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
       	base_url = "http://"+SMSEAGLE_IP+"/api/v2/"+method
       	query_args = {'login':SMSEAGLE_USER, 'pass':SMSEAGLE_PASSWORD, 'to':{rcpt}}
       	
       	match (SMSEAGLE_TYPE):
            case 'ring':
                query_args['duration':int(SMSEAGLE_DURATION)]
            case 'tts':
                query_args['message':msg]
                query_args['duration':int(SMSEAGLE_DURATION)]
            case 'tts_adv':
                query_args['message':msg]
                query_args['duration':int(SMSEAGLE_DURATION)]
                query_args['voice_id':int(SMSEAGLE_VOICE_ID)]
            case _:
                query_args['message':msg]
       	
       	url = base_url + '?' + encoded_args
       	
       	# Write log if logging enabled
       	if LOG_ENABLED:
       	    timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
       	    log.write("%s ===== BEGIN SENDING SMS ==== \n" % timestamp)			
       	    log.write("%s SMS recipient: %s\n" % (timestamp, rcpt))
       	    if SMSEAGLE_TYPE != 'ring':
       	        log.write("%s SMS text: %s\n" % (timestamp, msg))
			
       	#HTTP request to SMSEagle
       	result = requests.post(url, json = query_args)
    	
        # Write log if logging enabled
        if LOG_ENABLED:
            timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
            try:
                log.write("%s Sending result: %s\n" % (timestamp, result.text))
                log.write("%s ===== END SENDING SMS ====\n" % timestamp)
            finally:
                log.close()
    except Exception, e:
        print e
        sys.exit(1)
		
    
main()
