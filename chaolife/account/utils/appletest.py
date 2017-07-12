from chaolifeProject.settings import TEST

def isTestAccount(phone_number):
    if phone_number == '15726810000' or TEST:
        return True