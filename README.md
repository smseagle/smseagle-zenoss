Zenoss-SMS-EAGLE
================

Plugin for Zenoss to send SMS Alerts with SMSEagle device (http://www.smseagle.eu)

Script source: https://bitbucket.org/proximus/smseagle-zenoss/

Published on BSD License


Installation instructions
-------------------------

#### SMSEAGLE SETUP

1. Create a new user for this script in SMSEagle.

2. Open the **Access to API** menu, enable **APIv2** and generate an **access token**.

3. In the same menu, assign the right permissions (depending on what type of message/call you want to send)


#### ZENOSS SETUP

1. Download latest version of the script *zenoss_smseagle.py* from: https://bitbucket.org/proximus/smseagle-zenoss


2. Edit following lines in the script:

> **SMSEAGLE_TOKEN = "123abc456def"**\
> **SMSEAGLE_TYPE = "sms"**\
> **SMSEAGLE_IP = "192.168.0.101"**

Optionally, change the parameters required for TTS calls:
> **SMSEAGLE_DURATION = 10**\
> **SMSEAGLE_VOICE_ID = 1**


3. Save the script to the location: **$ZENHOME/bin/zenoss_smseagle.py** (where $ZENHOME is your Zenoss directory). Ensure that it's executable (chmod 755 zenoss_smseagle.py).


4. Add a cell phone number to the **"Pager"** field of each Zenoss user account.


5. Go to **Advanced->Settings** and modify the **"Page Command"** to: 
 
> $ZENHOME/bin/zenoss_smseagle.py $RECIPIENT


6. When finished, test by using the "test" link next to the cell number
shown in the Pager column of each user.


7. If testing is successful (a SMS message/call is received at the cell phone) create alerts in Zenoss and specify "page" as the action for an alert.
	

