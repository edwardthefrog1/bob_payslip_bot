from lib2to3.pgen2 import driver
from pip import main
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev
from selenium.webdriver.common.keys import Keys

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


class bob_bot:
    def __init__(self, person_id, xpaths_id='xero_x_paths'):
        self.person_id = person_id
        self.x_paths_id = xpaths_id
        self.login_details_dict = literal_eval_config(self.person_id)
        self.x_paths_dict = literal_eval_config(self.xpaths_id)

    def login(self):
        DRIVER_SAFARI.get(self.data_dict['url'])
        

    




def main():
    bob_bot_tom = bob_bot('tom')
    #bob_bot_tom.login()


if __name__ == "__main__":
    main()