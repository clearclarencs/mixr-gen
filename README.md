# mixR gen

This is a script to generate mixR account for referral rewards and signup rewards.

It includes a discord interface to generate the accounts or do this the old-fashioned way by running main.py.

If use_card is True it will add the card to the account which is required for the referral reward. Pass into the card a string of "ref_code cc_num cc_exp_month cc_exp_year_4_digits" which can also be passed in discord after !mixr.

Need to add your bot token to discord_interface.py before running (Don't even bother trying the one present).

Can use a cards.csv of cc_num,cc_exp_month,cc_exp_year_4_digits if you don't pass the card details in the card string.

Not much security on their API, SMS verification was easily bypassed by patching true to the customer details, email verification isn't required so a random (most likely fake) gmail is used and no IP detection is implemented so can be run all localhost.

I have also discovered, unique credit cards are not required, duplicate cards are still added and then deleted client side. So this bypasses that allowing you to reuse the same credit card and so there is no limit to the number of accounts someone could generate. Thats a serious fuck up on their behalf.

_Dont abuse this, it was mainly a way for me to learn to bypass SSL pinning and was a cool project to show off at the pub. If Stonegate are reading this, SSL pinning your app does not mean your API is secure. People will always sniff packets, (especially after a pint)._
