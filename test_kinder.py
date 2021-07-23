from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# db.collection.count()

"""
유치원 개수 db 개수 비교하는 것은 어려울 것 같다.
-> 예외 경우가 많음 (정보입력이 안된 유치원)
-> 어린이집은 폐원 필터링 안됨
=> selenium으로 count??
"""

## 마지막페이지 검사
def seleniumpage():
    driver = webdriver.Chrome('D:/Desktop/crawling_project/childschool/chromedriver.exe')
    driver.get('https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageCnt=50')


    kinder_btn = driver.find_element_by_css_selector("#filterArea > div.tabs > ul > li.tapMenu2 > a")
    kinder_btn.click()
    time.sleep(0.5)
    # close = driver.find_element_by_xpath("//*[@id='specseq-C-1']")
    # close.click()
    # rest = driver.find_element_by_xpath("//*[@id='specseq-C-2]")
    # rest.click()
    

        
    rest =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='specseq-C-1']")))
    rest.click()

    close =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='specseq-C-2']")))
    close.click()



    # for i in range(int(last_page), 0, -1): # (lstpg, 0, -1)
    # # for i in range(int(last_page), int(last_page)-1, -1):
    #     page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=50'.format(i) 


    # return last_page


def test_page():
    assert seleniumpage() == "687" # 마지막 페이지






