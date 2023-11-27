***___mixR gen___***

This is a script to generate mixR account for referral rewards and signup rewards.

It includes a discord interface to generate the accounts or do the old fashioned way by running main.py.

If use_card is True it will add the card to the account which is required for the referral reward. Pass into card a string of "ref_code cc_num cc_exp_month cc_exp_year_4_digits" which can also be passed in discord after !mixer.

Need to add your bot token to discord_interface.py before running (DOnt even bother trying the one present).

Can use a cards.csv of cc_num,cc_exp_month,cc_exp_year_4_digits if you dont pass the card details in card string.

Not much security on their API their sms verification is easily bypassed by patching true to the customer details and email verification isnt required so a random (most likely fake) gmail is used and no IP detection is implemented so can be ran all localhost.

*Dont abuse this, it was mainly a way for me to learn to bypass SSL pinning and was a cool project to show off at the pub. If mixr are reading this, SSL pinning your app does not mean your API is secure. People will always sniff packets, (especially after a pint).*
