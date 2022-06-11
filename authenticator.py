from pyotp import *
import time


def get_auth_code(secret_key):
    totp = TOTP(secret_key)
    while(True):
        if totp.verify(totp.now()) and (totp.now()):
            return str(totp.now())
        else:
            time.sleep(5)