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
    elif response.json().has_key('default_code') and response.json()['default_code'] == 603:
        # Invalid SMS default_code
        print(response.json()['default_code'])
        return False, "Invalid SMS default_code"
    else:
        return False, "尚未处理的错误"

# print(response.status_code)
# print(response.json()['default_code'])


def push_notification(putdata):
    url = 'https://api.leancloud.cn/1.1/push'
    print(url)
    print(json.dumps(putdata))
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(putdata))
    response.encoding = 'utf-8'
    # 使用异步
    print(response.text)
    print(response.status_code)
    print(response.request)
    if response.status_code == 200:
        return True, "Success"
    else:
        print(str(response.status_code))
        return False, "尚未处理的错误"








if __name__ == '__main__':
    push_notification()
    # send_register_sms()
    pass
