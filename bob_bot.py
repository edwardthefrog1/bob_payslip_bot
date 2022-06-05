from lib2to3.pgen2 import driver
from re import X
from pip import main
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep

DRIVER_SAFARI = webdriver.Safari()


def literal_eval_config(config_id):
    data_tmp, key_tmp = ([] for i in range(2))
    config = ConfigParser()
    config.read(CONFIG_PATH)
    config = dict(config.items(config_id))
    for key in config:
            data_tmp.append(litev(config[key]))
            key_tmp.append(key)
    return {key_tmp[i]: data_tmp[i] for i in range(len(key_tmp))}


def selenium_do_instructions(instructions_config_id, person_id):
    instr_dict = literal_eval_config(instructions_config_id)
    person_id_dict = literal_eval_config(person_id)
    for i, key in enumerate(instr_dict.keys()):
        DRIVER_SAFARI.implicitly_wait(10)
        if instr_dict[key][-1] == 'send_keys':
            print('sending key: {}'.format(instr_dict[key][0]))
            DRIVER_SAFARI.find_element(By.XPATH, instr_dict[key][0])\
                .send_keys(list(person_id_dict.values())[i])
        if instr_dict[key][-1] == 'click':
            print('click: {}'.format(instr_dict[key][0]))
            DRIVER_SAFARI.find_element(By.XPATH, instr_dict[key][0]).click()


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
        

def main():
    bob_bot_tom = bob_bot('tom')
    bob_bot_tom.login()
    #bob_bot_tom.logout()
    bob_bot_tom.close_safari()


if __name__ == "__main__":
    main()