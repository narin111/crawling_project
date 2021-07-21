from selenium import webdriver

## 마지막페이지 검사
def seleniumpage():
    driver = webdriver.Chrome('D:/Desktop/crawling_project/childschool/chromedriver.exe')
    driver.get('https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageCnt=50')

    last_page = driver.find_element_by_css_selector('#resultArea > div.footer > div.paging > a.last').get_attribute("href")
    last_page = last_page.split("=")[1]

    # for i in range(int(last_page), 0, -1): # (lstpg, 0, -1)
    # # for i in range(int(last_page), int(last_page)-1, -1):
    #     page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=50'.format(i) 

    return last_page


def test_page():
    assert seleniumpage() == "687" # 마지막 페이지






