from selenium import webdriver
import os
from mysite.settings import BASE_DIR
print(os.getcwd())

def process(s):
    # path = str(os.path.join(BASE_DIR, 'food'))
    # print(path+'\\geckodriver.exe')
    driver = webdriver.Firefox(os.path.join(BASE_DIR,''))
    driver.get(f'https://in.search.yahoo.com/search?p={s}')


    search_go = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/ol/li[1]/div/div/ul/li[4]/a')
    search_go.click()

    detail = []

    i = 1
    for i in range(1,6):
        try:
            temptitle = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div/ol/li[{i}]/div/ul/li/h4/a')

            tempimg = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div/ol/li[{i}]/div/ul/li/a/img').get_attribute('src')

            temptime = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div/ol/li[{i}]/div/ul/li/span[2]')

            temptxt = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div/ol/li[{i}]/div/ul/li/p')

            templink = temptitle.get_attribute('href')
            detail.append([temptitle.text,tempimg,temptime.text,temptxt.text,templink])
        except:
            pass


    driver.close()
    driver.quit()



    return detail

    
        