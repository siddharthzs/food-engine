from selenium import webdriver
import os
from mysite.settings import BASE_DIR

def peak(s):
    # path = str(os.path.join(BASE_DIR, 'food'))
    # # print(path+'\\geckodriver.exe')
    driver = webdriver.Firefox(os.path.join(BASE_DIR,''))
    # driver = webdriver.Firefox()
    driver.get(f'https://www.productreview.com.au/search?showDiscontinued=true&q={s}')


    # search_go = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[1]/div[1]/div/span/div/div/div/div/div[2]/div[3]/div/div[1]/h2/a')
    # search_go.click()

    detail = []

    i = 1
    for i in range(1,15):
        try:
            temptitle = driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div[{i}]/div/div/div/div/div[1]/a/p/span/span[2]')
            detail.append(temptitle.text[:15])
        except:
            pass


    driver.close()
    driver.quit()


    return detail
