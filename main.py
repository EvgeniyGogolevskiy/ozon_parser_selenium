import undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

url = 'https://www.ozon.ru/category/smartfony-15502/?sorting=rating'
qq = 0
links = []

try:
    browser = undetected_chromedriver.Chrome()
    browser.get(url)
    time.sleep(3)
    for _ in range(3):
        a = browser.find_elements(By.CLASS_NAME, "k5s")
        for i in a:
            qq += 1
            href = i.find_element(By.TAG_NAME, "a").get_attribute('href')
            print(f'{qq}, {href}')
            print('-----------------')
            links.append(href)
            time.sleep(0.3)
            if qq == 100:
                break
        # nex = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[2]/a")
        actions = ActionChains(browser)
        actions.move_to_element(i)
        actions.perform()
        time.sleep(5)
except Exception as error:
    print(error)
finally:
    browser.close()
    browser.quit()

res = []
ll = []

for link in links:
    try:
        browse = undetected_chromedriver.Chrome()
        browse.get(link)
        time.sleep(1.5)
    except Exception as er:
        print(er)
        browse.close()
        browse.quit()
        time.sleep(2)
        continue
    try:
        xx = browse.find_element(By.LINK_TEXT, "Перейти к описанию")
        xx.click()
        time.sleep(1)
        x = browse.find_elements(By.CLASS_NAME, "ly9")
    except Exception as er:
        print(er)
        browse.close()
        time.sleep(0.5)
        continue
    for i in x:
        if ('Android ' in i.text) or ('iOS ' in i.text):
            ll.append(i.text)
        else:
            continue
    browse.close()
    time.sleep(0.5)

df = pd.DataFrame(list(map(lambda x: x.split(' '), ll)), columns=['Brend', 'Version'])
df['rn'] = 1
df = pd.DataFrame(df.groupby(['Brend', 'Version'])['rn'].count()).reset_index().sort_values(by=['Brend', 'rn'],
                                                                                            ascending=[True, True])
df['Brend_Version'] = df['Brend'] + "_" + df['Version']