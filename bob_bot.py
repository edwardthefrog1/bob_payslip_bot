from lib2to3.pgen2 import driver
from re import X
from tkinter import N
from pip import main
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from authenticator import get_auth_code

print('Start bob bot with webdriver ? (y/n)')
while(True):    
    reply = input()
    if reply == 'y' or reply == 'Y':
        DRIVER_SAFARI = webdriver.Safari()
        break
    elif reply == 'n' or reply == 'N':
        break
    else:
        print('invalid input, please answer with (y/n)')

def literal_eval_config(config_id):
    data_tmp, key_tmp = ([] for i in range(2))
    config = ConfigParser()
    config.read(CONFIG_PATH)
    config = dict(config.items(config_id))
    for key in config:
            data_tmp.append(litev(config[key]))
            key_tmp.append(key)
    return {key_tmp[i]: data_tmp[i] for i in range(len(key_tmp))}

def write_to_config(key, param, data):
    config = ConfigParser()
    config.read(CONFIG_PATH)
    config.set(key, param, str(data))
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def selenium_do_instructions(instructions_config_id, data_id):
    sleep(5)
    try:
        DRIVER_SAFARI.switch_to().defaultContent()
    except:
        print('could not find default frame')
    instr_dict = literal_eval_config(instructions_config_id)
    data_id_dict = literal_eval_config(data_id)
    for i, key in enumerate(instr_dict.keys()):

        if instr_dict[key][-1] == 'XPATH':
            if instr_dict[key][1] == 'send_keys':
                print('sending key: {}'.format(instr_dict[key][0]))
                DRIVER_SAFARI.find_element(By.XPATH, \
                    instr_dict[key][0]).send_keys(list(data_id_dict.values())[i])
            if instr_dict[key][1] == 'click':
                print('click: {}'.format(instr_dict[key][0]))
                DRIVER_SAFARI.find_element(By.XPATH, \
                    instr_dict[key][0]).click()

        if instr_dict[key][-1] == 'CLASS_NAME':
            if instr_dict[key][1] == 'send_keys':
                print('sending key: {}'.format(instr_dict[key][0]))
                DRIVER_SAFARI.find_element(By.CLASS_NAME, \
                    instr_dict[key][0]).send_keys(list(data_id_dict.values())[i])
            if instr_dict[key][1] == 'click':
                print('click: {}'.format(instr_dict[key][0]))
                DRIVER_SAFARI.find_element(By.CLASS_NAME, \
                    instr_dict[key][0]).click()


class bob_bot:
    def __init__(self, person_id):
        self.person_id = person_id

    def login(self):
        DRIVER_SAFARI.get(literal_eval_config(self.person_id)['url'])
        selenium_do_instructions('login_instructions', self.person_id)

    def logout(self):
        selenium_do_instructions('logout_instructions', self.person_id)

    def close_safari(self):
        DRIVER_SAFARI.quit()

    def authenticate_bob(self):
        auth_code = get_auth_code(literal_eval_config(self.person_id)['secret_key'])
        write_to_config('auth_data', 'auth_code', auth_code)
        selenium_do_instructions('authenticate_instructions', 'auth_data')
        

def main():
    bob_bot_tom = bob_bot('tom')
    bob_bot_tom.login()
    bob_bot_tom.authenticate_bob()
    #bob_bot_tom.logout()
    #bob_bot_tom.close_safari()


if __name__ == "__main__":
    main()