#! /usr/bin/env python
# ============================== SUMMARY =====================================
#
# Program : zenoss_smseagle.py
# Version : 1.0
# Date : May 13 2013
# Author : SMSEagle Team
# Summary : This plugin sends ZenOss SMS alerts with SMSEagle hardware sms gateway
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
import urllib
import urllib2

# Edit these settings to match your own
SMSEAGLE_USER = "john"
SMSEAGLE_PASSWORD = "doe"
SMSEAGLE_IP = "192.168.0.101"
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

       	# Prepare HTTP request
       	base_url = "http://"+SMSEAGLE_IP+"/index.php/http_api/send_sms"
       	query_args = { 'login':SMSEAGLE_USER, 'pass':SMSEAGLE_PASSWORD, 'to':rcpt, 'message':msg}
       	encoded_args = urllib.urlencode(query_args)
       	url = base_url + '?' + encoded_args
       	
       	# Write log if logging enabled
       	if LOG_ENABLED:
       	    timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
       	    log.write("%s ===== BEGIN SENDING SMS ==== \n" % timestamp)			
       	    log.write("%s SMS recipient: %s\n" % (timestamp, rcpt))
       	    log.write("%s SMS text: %s\n" % (timestamp, msg))
			
       	#HTTP request to SMSEagle
       	result = urllib2.urlopen(url).read()
    	
        # Write log if logging enabled
        if LOG_ENABLED:
            timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
            try:
                log.write("%s Sending result: %s\n" % (timestamp, result))
                log.write("%s ===== END SENDING SMS ====\n" % timestamp)
            finally:
                log.close()
    except Exception, e:
        print e
        sys.exit(1)
		
    
main()
