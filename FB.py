import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dhooks import Webhook, Embed
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

file = open('config.txt', 'r')
link = file.readline().strip('Link: ').strip()
wh = file.readline().strip('WebHook: ').strip()
file.close()

option = webdriver.ChromeOptions()
option.add_argument('incognito')
option.add_argument('headless')

browser = webdriver.Chrome(executable_path='D:\Downloads\chromedriver_win32\chromedriver.exe', 
                           options=option)

browser.get(link)

timeout = 10

try:
    WebDriverWait(browser, timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[3]/a/div/i')))
except TimeoutException:
    print('Timed out waiting for page to load$$')
    browser.quit()

#initial_post = browser.find_elements_by_class_name('story_body_container')

initial_post = browser.find_elements_by_class_name('_3w8y')


first = initial_post[1].text

while True:
    print('Monitoring target$$')
    browser.refresh()
    new_post = browser.find_elements_by_class_name('_3w8y')
    new = new_post[1].text

    disclaimer = 'THIS CONTENT IS PROVIDED “AS IS” AND IS SUBJECT TO CHANGE OR REMOVE WITHOUT NOTICE. PROMO CODES, IF ANY, MAY EXPIRE AT ANY TIME. #AD'
    
    if disclaimer in new:
        new = new.strip(disclaimer)

    if new != first:
        print('$$NEW POST FOUND$$')
        first = new
        hook = Webhook(wh)
        embed = Embed(description='', color=0x1e0f3, timestamp='now')
        #embed.set_author(name='Facebook Monitor')
        #embed.add_field('Product', value=product)
        embed.add_field(name='Content', value=new)
        embed.set_footer(text='By @samoculus', icon_url='https://pbs.twimg.com/profile_images/1210468558431555585/2oDzopV3_400x400.jpg')
        try: 
            hook.send(embed=embed)
        except:
            print('Send failed$$')
    time.sleep(15)