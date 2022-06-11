from lib2to3.pgen2 import driver
from selenium import webdriver
from main import CONFIG_PATH
from configparser import ConfigParser
from ast import literal_eval as litev
from selenium.webdriver.common.by import By
from authenticator import get_auth_code
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def setup_run():
    users_dict = literal_eval_config('auth_code_recipients')
    print('Want auth code? (y/n):', end='')
    while(True):    
        reply = input()
        if reply == 'y' or reply == 'Y':
            print('\nSelect auth code recipient:{}'.format(users_dict.keys()))
            print('I.e: type reply as: ["recipient", "recipient2"]')
            print('Type users here: ', end='')
            try:
                user_s_list = litev(input())
                for i, user_s in enumerate(user_s_list):
                    print('auth code: {}'.format(get_auth_code(literal_eval_config(user_s)\
                    ['secret_key'])))
            except TypeError:
                print('could not enumerate list.. please restart and input list')
                quit()
            break
        elif reply == 'n' or reply == 'N':
            break
        else:
            print('invalid input, please answer with (y/n)')
    print('Start bob bot with webdriver ? (y/n):', end='')
    while(True):    
        reply = input()
        if reply == 'y' or reply == 'Y':
            create_driver = True
            break
        elif reply == 'n' or reply == 'N':
            create_driver = False
            break
        else:
            print('invalid input, please answer with (y/n)')
    print('quit or continue from here? (y/n):', end='')
    while(True):    
        reply = input()
        if reply == 'y' or reply == 'Y':
            break
        elif reply == 'n' or reply == 'N':
            quit()
        else:
            print('invalid input, please answer with (y/n)')
    return user_s_list, create_driver


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


def selenium_do_instructions(instructions_config_id, data_id, driver_safari):
    scraped_data = []
    instr_dict = literal_eval_config(instructions_config_id)
    if data_id != None:
        data_id_dict = literal_eval_config(data_id)
    for i, key in enumerate(instr_dict.keys()):    
        if instr_dict[key][-1] == 'XPATH':
            by_format = By.XPATH
        if instr_dict[key][-1] == 'TAG_NAME':
            by_format = By.TAG_NAME
        if instr_dict[key][-1] == 'CLASS_NAME':
            by_format = By.CLASS_NAME  
        element = WebDriverWait(driver_safari, 30).until\
            (EC.presence_of_element_located((by_format, instr_dict[key][0])))
        print(element)
        if instr_dict[key][1] == 'send_keys':
            print('sending key: {}'.format(instr_dict[key][0]))
            driver_safari.find_element(by_format, \
                instr_dict[key][0]).send_keys(list(data_id_dict.values())[i])
        if instr_dict[key][1] == 'click':
            print('click: {}'.format(instr_dict[key][0]))
            driver_safari.find_element(by_format, \
                instr_dict[key][0]).click()
        if instr_dict[key][1] == 'scrape':
            print('scrape: {}'.format(instr_dict[key][0]))
            scrape_list = driver_safari.find_elements(by_format,\
                instr_dict[key][0])
            for j, scrape in enumerate(scrape_list):
                scraped_data.append(scrape.text)
                print(scraped_data[j])
                

def create_bobs(users, create_driver):
    bob_bot_list = []
    if create_driver == True:
        for i, user_s in enumerate(users):
            bob_bot_list.append(bob_bot(user_s, webdriver.Safari()))
    else:
        print('not creating bots: no webdriver')
        quit()
    return bob_bot_list

def login_bob_bots(bob_bot_list):
    for i, user_s in enumerate(bob_bot_list):
        print('Logging in {} ...'.format(bob_bot_list[i]))
        user_s.login()
        user_s.authenticate_bob()
    return bob_bot_list


class bob_bot:
    def __init__(self, person_id, driver_safari):
        self.person_id = person_id
        self.driver_safari = driver_safari

    def login(self):
        self.driver_safari.get(literal_eval_config(self.person_id)['url'])
        selenium_do_instructions('login_instructions', self.person_id, \
            self.driver_safari)

    def logout(self):
        selenium_do_instructions('logout_instructions', self.person_id, \
            self.driver_safari)

    def close_safari(self):
        self.driver_safari.quit()

    def authenticate_bob(self):
        auth_code = get_auth_code(literal_eval_config(self.person_id)\
            ['secret_key'])
        write_to_config('auth_data', 'auth_code', auth_code)
        selenium_do_instructions('authenticate_instructions', 'auth_data', \
            self.driver_safari)
    
    def get_profile_data(self):
        selenium_do_instructions('get_profile_data_instructions', None,\
             self.driver_safari)
    
    def get_payslips_data(self):
        pass

    def get_leave_data(self):
        pass

    def get_timesheet_data(self):
        pass



def main():
    user_s_list, create_driver = setup_run()
    bob_bot_list = login_bob_bots(create_bobs(user_s_list, create_driver))
    bob_bot_list[0].get_profile_data()
    sleep(30)
if __name__ == "__main__":
    main()