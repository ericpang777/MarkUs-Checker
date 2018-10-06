from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import six, base64

file = open('config.txt', 'r', encoding='utf-8')
USERNAME = file.readline().rstrip()
PASSWORD = file.readline().rstrip()
KEY = file.readline().rstrip()
file.close()

CSCA08 = 'https://markus.utsc.utoronto.ca/csca08f18'
CSCA67 = 'https://markus.utsc.utoronto.ca/csca67f18'

def decode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

browser = webdriver.Firefox()
browser.get((CSCA08))

username_field = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'user_login')))
username_field.send_keys(decode(KEY, USERNAME))

password_field = browser.find_element_by_id('user_password')
password_field.send_keys(decode(KEY, PASSWORD))
next_button = browser.find_element_by_name('commit')
next_button.click()

result_box = browser.find_element_by_xpath('//*[@id="content"]/div[7]/div/table/tbody/tr[last()]/td[3]')
print(result_box.text)
#if result_box.text != 'No marks are available yet.':
#    print(result_box.text)
