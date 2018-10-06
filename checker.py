from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = ''
PASSWORD = ''
CSCA08 = 'https://markus.utsc.utoronto.ca/csca08f18'
CSCA67 = 'https://markus.utsc.utoronto.ca/csca67f18'

browser = webdriver.Firefox()
browser.get((CSCA08))

username_field = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'user_login')))
username_field.send_keys(USERNAME)

password_field = browser.find_element_by_id('user_password')
password_field.send_keys(PASSWORD)
next_button = browser.find_element_by_name('commit')
next_button.click()

result_box = browser.find_element_by_xpath('//*[@id="content"]/div[7]/div/table/tbody/tr[last()]/td[3]')
print(result_box.text)
#if result_box.text != 'No marks are available yet.':
#    print(result_box.text)