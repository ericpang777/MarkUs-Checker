from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from win10toast import ToastNotifier
import time
from datetime import datetime
import traceback

file = open('config.txt', 'r', encoding='utf-8')
USERNAME = file.readline().rstrip()
PASSWORD = file.readline().rstrip()
KEY = file.readline().rstrip()
CSCA08 = file.readline().rstrip()
CSCA67 = file.readline().rstrip()
file.close()


def decode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def get_class(class_url):
    browser = webdriver.Firefox(options=options)
    browser.get(class_url)

    username_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user_login')))
    username_field.send_keys(decode(KEY, USERNAME))

    password_field = browser.find_element_by_id('user_password')
    password_field.send_keys(decode(KEY, PASSWORD))
    next_button = browser.find_element_by_name('commit')
    next_button.click()

    result_box = browser.find_element_by_xpath('//*[@id="content"]/div[7]/div/table/tbody/tr[last()]/td[3]')
    print(datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
    if result_box.text != 'No marks are available yet.':
        toaster.show_toast('MarkUs ' + class_url[-9:-3].upper(), 'Mark Updated')
        global updated_mark
        updated_mark = True
        print('MarkUs ' + class_url[-9:-3].upper(), 'Mark Updated')
        print(result_box.text + '\n')
    else:
        toaster.show_toast('MarkUs ' + class_url[-9:-3].upper(), 'No Update')
        print('MarkUs ' + class_url[-9:-3].upper(), 'No update')
        print(result_box.text + '\n')
    browser.quit()


toaster = ToastNotifier()
options = Options()
options.headless = True
updated_mark = False

try:
    while not updated_mark:
        get_class(CSCA08)
        get_class(CSCA67)
        time.sleep(1500)
except Exception as e:
    traceback.print_exc()

raise SystemExit()