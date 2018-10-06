from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from win10toast import ToastNotifier
import time
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
    browser.get(class_url)

    username_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user_login')))
    username_field.send_keys(decode(KEY, USERNAME))

    password_field = browser.find_element_by_id('user_password')
    password_field.send_keys(decode(KEY, PASSWORD))
    next_button = browser.find_element_by_name('commit')
    next_button.click()

    result_box = browser.find_element_by_xpath('//*[@id="content"]/div[7]/div/table/tbody/tr[last()]/td[3]')
    if result_box.text != 'No marks are available yet.':
        toaster.show_toast('MarkUs ' + class_url[-9:-3].upper(), 'Mark Updated')
        global updated_mark
        updated_mark = True
        print(result_box.text)
    else:
        toaster.show_toast('MarkUs ' + class_url[-9:-3].upper(), 'No Update')
        print(result_box.text)

toaster = ToastNotifier()
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
updated_mark = False

try:
    while not updated_mark:
        browser = webdriver.Firefox(options=options)
        get_class(CSCA08)
        get_class(CSCA67)
        browser.quit()
        time.sleep(1500)
except Exception as e:
    traceback.print_exc()
    browser.quit()
