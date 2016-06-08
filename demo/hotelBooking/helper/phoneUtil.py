
def verifySmsCode(mobilePhone,smscode):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {
        modelKey.KEY_LEAN_PHONENUMBER: str(phoneNumber),
        "template": "register",
    }
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(values), headers=headers)
    # 使用异步
    print(response.status_code)
    print(str(response.content))
    return JSONWrappedResponse(status=1, message="发送成功")