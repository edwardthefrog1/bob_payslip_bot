from lib2to3.pgen2 import driver
from pip import main
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev

DRIVER_SAFARI = webdriver.Safari()


class bob_bot:
    def __init__(self, person_id):
        self.person_id = person_id
        self.data_dict

    def get_data_dict(self):
        data_tmp, key_tmp = ([] for i in range(2))
        config = ConfigParser()
        config.read(CONFIG_PATH)
        config = dict(config.items(self.person_id))
        for key in config:
            data_tmp.append(litev(config[key]))
            key_tmp.append(key)
        self.data_dict = {key_tmp[i]: data_tmp[i] for i in range(len(key_tmp))}

    def login(self):
        DRIVER_SAFARI.get(self.data_dict['url'])

    




def main():
    bob_bot_tom = bob_bot('tom_xero')
    bob_bot_tom.get_data_dict()
    bob_bot_tom.login()



if __name__ == "__main__":
    main()