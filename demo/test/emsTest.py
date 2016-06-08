import requests
import json

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"


def send_register_sms():
    # support voice or sms
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {"mobilePhoneNumber": "15726816099",
              "template": "register",
              'smsType': 'sms'
              }
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(values), headers=headers)
    print(response)
    print(response.content)
    print(response.status_code)


def verifySmsCode(mobilePhoneNumber, smscode):
    url = 'https://api.leancloud.cn/1.1/verifySmsCode/' + str(smscode)
    print(url)
    values = {
        "mobilePhoneNumber": str(mobilePhoneNumber),
    }
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, params=values)
    response.encoding = 'utf-8'
    # 使用异步
    print(response.content)
    print(response.status_code)
    if response.status_code == 200:
        return True, "Success"
    elif response.json().has_key('code') and response.json()['code'] == 603:
        # Invalid SMS code
        print(response.json()['code'])
        return False, "Invalid SMS code"
    else:
        return False, "尚未处理的错误"

# print(response.status_code)
# print(response.json()['code'])


if __name__ == '__main__':
    verifySmsCode(15726816099, 200792)
    # send_register_sms()
    pass
