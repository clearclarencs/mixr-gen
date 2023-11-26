import requests, traceback, time, qrcode, random, string
# from smsactivate.api import SMSActivateAPI
from PIL import Image, ImageDraw, ImageFont


def gen(use_card=False, card=""):
    ref_code = ""
    if use_card:
        ref_code = "rfwvwbwz"
    email = f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(10,15)))}@gmail.com"
    print(email)

    if use_card and card=="":
        with open("cards.csv", "r") as r:
            cards = r.read().splitlines()
        card = cards.pop(-1)
        with open("cards.csv", "w") as w:
            w.write("\n".join(cards))
        print(card)
        if len(card.split(",")) == 4:
            ref_code, cc_num, cc_exp_mon, cc_exp_yr = card.split(",")
        elif len(card.split(",")) == 3:
            cc_num, cc_exp_mon, cc_exp_yr = card.split(",")
        else:
            ref_code = card
    elif use_card:
        cc_num, cc_exp_mon, cc_exp_yr = card.split(" ")


    sesh = requests.session()
    sesh.headers.update({"Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    })

    # Get auth token
    r = sesh.post("https://atreemo.emails.mixr.co.uk/token", 
        data={"username":"hello@mixr.co.uk","password":"Vakhyx-fokkoh-4jotzi","grant_type":"password"}
        )

    try:
        atree_token = r.json()['access_token']

        sesh.headers.update({
            "Authorization": f"Bearer {atree_token}",
            "Content-Type": "application/json"
        })

        # create account
        r = sesh.post("https://atreemo.emails.mixr.co.uk/api/Customer/Post",
            json={
                "PersonalInfo":{
                    "FirstName":''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(10,15))),
                    "LastName":''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(10,15))),
                    "Email": email,
                    "MobilePhone":""
                },
                "ExternalIdentifier":{
                    "ExternalID":"1243",
                    "ExternalSource":"MiXR App"
                },
                "Referrer":{
                    "ReferredByCode": ref_code
                },
                "MarketingOptin":{
                    "EmailOptin":False,
                    "SmsOptin":False
                },
                "SupInfo":[ # Hard code password
                    {"FieldName":"HashPassword","FieldContent":"$argon2id$v=19$m=65536,t=5,p=2$uhoR0kpxfLxp/O/LRtHiYw$cTHuSSaruIkfcgwMGLWYVBWFJNDkZhSu8OlcqM05/Hg"}
                ],
                "MemberNumber":{"GenerateMemberNumber":True}
            } 
        )
        ctcId = r.json()["ResponseData"]["CtcID"]
        memNum = r.json()["ResponseData"]["MemberNumber"]

        r = sesh.patch("https://atreemo.emails.mixr.co.uk/api/Customer/Patch",
            headers = {"Authorization": f"Bearer {atree_token}"},
            json = {"CtcID":ctcId,"SupInfo":[{"FieldName":"2FAMobileNumberValidated","FieldContent":"true"}, {"FieldName":"FirstTimeRewardView","FieldContent":"true"}]}
                    
        )

        if use_card:
            sesh.headers.pop("Authorization")

            # Auth card
            r = sesh.post("https://core.spreedly.com/v1/payment_methods/restricted.json?from=iframe&v=1.115",
                headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 11; sdk_gphone_arm64 Build/RSR1.210722.013.A6; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36",
                    "Spreedly-Environment-Key": "1Lf7DiKgkcx5Anw7QxWdDxaKtTa",
                    "Accept": "*/*",
                    "Origin": "https://core.spreedly.com",
                    "X-Requested-With": "com.stonegate.mixr",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://core.spreedly.com/v1/embedded/number-frame-1.115.html",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9"
                },
                json={
                    "environment_key":"1Lf7DiKgkcx5Anw7QxWdDxaKtTa",
                    "payment_method":{
                        "allow_blank_name":"true",
                        "credit_card":{
                            "number": cc_num,  # Card num
                            "verification_value": "",
                            "month": cc_exp_mon,
                            "year": cc_exp_yr
                        }
                    }
                }
            )
            card_auth = r.json()["transaction"]

            # Get bink token
            r = sesh.post("https://api.gb.bink.com/v2/token",
                headers={
                    "Authorization": "Basic Y29tLnN0b25lZ2F0ZS5taXhyOndHQkpIaEtFVzdScFN5czU0dUdTMlV3OUdvbzNBWUg2MndZa2paTEJXaGQ1ZTVBbkhE",
                },
                json={
                    "grant_type": "client_credentials",
                    "username": email,
                    "scope": [
                        "user"
                    ]
                }
            )

            sesh.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})

            # Prep card add
            r = sesh.post("https://api.gb.bink.com/v2/loyalty_cards/add_trusted",
                json={
                    "loyalty_plan_id": 393,
                    "account": {
                        "add_fields": {
                            "credentials": [
                                {
                                    "credential_slug": "card_number",
                                    "value": memNum
                                }
                            ]
                        },
                        "merchant_fields": {
                            "account_id": memNum
                        }
                    }
                }
            )

            # Add card
            r = sesh.post("https://api.gb.bink.com/v2/payment_accounts",
                json={
                    "expiry_month": str(int(cc_exp_mon)),
                    "expiry_year": cc_exp_yr,
                    "token": card_auth["payment_method"]["token"],
                    "last_four_digits": cc_num[-4:],
                    "first_six_digits": cc_num[0:6],
                    "fingerprint": card_auth["payment_method"]["fingerprint"]
                }
            )
            sesh.headers.update({"Authorization": f"Bearer {atree_token}"})

            
        r = sesh.patch("https://atreemo.emails.mixr.co.uk/api/Customer/Patch",
            headers = {"Authorization": f"Bearer {atree_token}"},
            json = {"CtcID":ctcId,"SupInfo":[{"FieldName":"pll_mixr","FieldContent":"true"}]}
            )
        

        time.sleep(2)
        r = sesh.get(f"https://atreemo.emails.mixr.co.uk/api/Voucher/GetByCustomerID?customerid={ctcId}")

        voucherCode = r.json()["voucher"][0]["VoucherCode"]

        img = qrcode.make(voucherCode, box_size=19, border=0)

        img1 = Image.open(r"bg.png")
        img1.paste(img, (180,750)) 

        draw = ImageDraw.Draw(img1)
        font = ImageFont.truetype('Arial', 25)
        draw.text((320, 1270), voucherCode, font=font, fill="black")

        return img1

    except Exception as e:
        print(traceback.format_exc())
        print(r.status_code, r.url, r.text)

if __name__ == "__main__":
    gen(use_card=True).save("code.png")