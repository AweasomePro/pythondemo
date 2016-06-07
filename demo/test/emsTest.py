import requests
import json
APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"

def send_register_sms():
    # url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    # values = {"mobilePhoneNumber": 15726814574}
    # jdata = json.dumps(values)
    # req = urllib.request.Request(url, jdata)
    # print(req.get_method())
    # req.add_header('X-LC-Id', APP_ID)
    # req.add_header('X-LC-Key', APP_KEY)
    # req.add_header('Content-Type', 'application/json')
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {"mobilePhoneNumber": "15726814574"}
    headers = {'X-LC-Id':APP_ID,'X-LC-Key':APP_KEY,'Content-Type':'application/json'}
    response = requests.post(url,data=json.dumps(values),headers = headers)
    print(type(response))
    print(response)


if __name__ == '__main__':
    send_register_sms()
    pass
