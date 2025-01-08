Zenoss-SMS-EAGLE
================

Plugin for Zenoss to send SMS Alerts with SMSEagle device (http://www.smseagle.eu)

Script source: https://bitbucket.org/proximus/smseagle-zenoss/

Published on BSD License


Installation instructions
-------------------------

#### SMSEAGLE SETUP

Create a new user for this script in SMSEagle.


#### ZENOSS SETUP

1. Download latest version of the script *zenoss_smseagle.py* from: https://bitbucket.org/proximus/smseagle-zenoss


2. Edit following lines in the script:

    SMSEAGLE_USER = "john"
    
	SMSEAGLE_PASSWORD = "doe"
    
	SMSEAGLE_IP = "192.168.0.101"


	Save the script to the location: $ZENHOME/bin/zenoss_smseagle.py (where $ZENHOME is your Zenoss directory). Ensure that it's executable (chmod 755 zenoss_smseagle.py).


3. Add a cell phone number to the "Pager" field of each Zenoss user account.


4. Go to Advanced->Settings and modify the "Page Command" to: 
 
     $ZENHOME/bin/zenoss_smseagle.py $RECIPIENT


5. When finished, test by using the "test" link next to the cell number
shown in the Pager column of each user.


6. If testing is successful (a SMS message is received at the cell phone) create alerts in Zenoss and specify "page" as the action for an alert.
	

