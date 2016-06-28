
def phone_is_legal(phone_number):
    phoneprefix=['130','131','132','133','134','135','136','137','138','139','150','151','152','153',
                 '156','157','158','159','170','183','182','185','186','188','189']
    if len(phone_number)!=11:
        return True
    else:
        # 检测是否全部是数字
        if phone_number.isdigit():
            if phone_number[:3] in phoneprefix:
                return True
            else:
                return False

