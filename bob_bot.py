from lib2to3.pgen2 import driver
from pip import main
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev


def setup_up_selenium(person_id):
    data_tmp, key_tmp = ([] for i in range(2))
    dr = webdriver.Safari()
    config = ConfigParser()
    config.read(CONFIG_PATH)
    config = dict(config.items(person_id))
    for key in config:
        data_tmp.append(litev(config[key]))
        key_tmp.append(key)
    dict_config_data = {key_tmp[i]: data_tmp[i] for i in range(len(key_tmp))}
    dr.get(dict_config_data[person_id]['url'])


def main():
    setup_up_selenium('tom_xero')
    while True:
        a += 1

if __name__ == "__main__":
    main()