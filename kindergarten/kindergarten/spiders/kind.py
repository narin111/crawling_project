import enum
import scrapy
from selenium import webdriver
import time
import pymongo

## git push test

path = 'C:/Users/LG/Desktop/scrapy_prac/pagescrapy/chromedriver.exe'
driver = webdriver.Chrome(path)

# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client.dbkindergarden # local

# connection = pymongo.MongoClient("mongodb+srv://{}:{}@rbscrapycluster.hzuaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(os.getenv('ID'), os.getenv('PWD')))
connection = pymongo.MongoClient("mongodb+srv://readwrite-alldb:X8KkW5nnLzNa4q3l@rbcluster.2lhlu.mongodb.net/test")
db = connection.kinder_test


#### 어린이집
class KindSpider(scrapy.Spider):
    name = 'kind'

    def start_requests(self):
        # pageCnt = 50 or 10
        yield scrapy.Request(url="https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageCnt=50", callback=self.parse_childpage)
        # return super().start_requests()


    def parse_childpage(self, response):
        last_page = response.css('#resultArea > div.footer > div.paging > a.last::attr(href)').get()
        last_page = last_page.split("=")[1]
        print("\n\n======lastpage==========")
        print(int(last_page))
        print("========================")
        
        for i in range(int(last_page), 686, -1): # (lstpg, 0, -1)
        # for i in range(1, 5):
        # pageCnt = 50
            page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=50'.format(i) ##pageCnt=50으로 바꾸기
            # 개발자 도구에서 network 창 headers에 들어가면 파라미터를 통해서 페이지를 보일 수 있는 정보를 조절할 수 있다.
            yield scrapy.Request(url = page_url, callback = self.parse_allchild, meta={'page_kinder':page_url})


    # 어린이집 정보 가져오기
    def parse_allchild(self, response):
       

        driver.get(response.meta['page_kinder']) 
       
        # 어린이집 선택 => 어린이집 테스트
        baby = driver.find_element_by_css_selector("#filterArea > div.tabs > ul > li.tapMenu3 > a")
        baby.click()

        
        # 페이지에서 유치원/어린이집 리스트 개수 
        kinder_list = driver.find_elements_by_css_selector("#resultArea > div.lists > ul > li")
        
        # for i in range(1, 3):
        for i in range(1, len(kinder_list)+1):   
            baby_or_kinder = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > span".format(i)).text
            print("\n\n"+baby_or_kinder+"\n\n")
            if(baby_or_kinder == "유"):
                ## 함수이동
                print("\n\n유치원")
            elif(baby_or_kinder == "어"):
                print("\n\n어린이집") 

                kinder_one = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > a".format(i))
                kinder_one.click()

                # 활성탭 바꾸기
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)

                
                kinder_name = driver.find_element_by_css_selector("#CRNAMETITLE").text
                kinder_chief = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(3) > td").text
                kinder_esta = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(4) > td").text
                kinder_admin = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(6) > td").text
                kinder_call = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(7) > td").text
                kinder_homep = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(8) > td").text
                kinder_opertime = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(9) > td").text
                kinder_addr = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table > tbody > tr:nth-child(10) > td").text


                # 영유아 및 교직원 탭 클릭(현원수/총정원)
                kinder_basic = driver.find_element_by_css_selector("#popWrap2 > div > div > ul > li:nth-child(3) > a")
                kinder_basic.click()

                # 인원수 테이블 테스트 for문 하나로 합치기
                per_table = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table:nth-child(3)")
                tbody = per_table.find_element_by_tag_name("tbody")
                rows_class = tbody.find_elements_by_tag_name("tr")[0]
                body = rows_class.find_elements_by_tag_name("td")
                for index, value in enumerate(body):
                    if(index == 0):
                        kinder_totnum = value.text
                    elif(index == 1):
                        kinder_currnum = value.text
                    elif(index == 3):
                        kinder_0cls = value.text
                    elif(index == 4):
                        kinder_1cls = value.text
                    elif(index == 5):
                        kinder_2cls = value.text
                    elif(index == 6):
                        kinder_3cls = value.text
                    elif(index == 7):
                        kinder_4cls = value.text
                    elif(index == 8):
                        kinder_5cls = value.text
                    elif(index == 9):
                        kinder_mix1 = value.text 
                    elif(index == 10):
                        kinder_mix2 = value.text
                    elif(index == 11):
                        kinder_spcls = value.text
                    elif(index == 12):
                        kinder_after = value.text
                    elif(index == 13):
                        kinder_etccls = value.text

                rows_totnum = tbody.find_elements_by_tag_name("tr")[1]
                body = rows_totnum.find_elements_by_tag_name("td")
                for index, value in enumerate(body):
                    if(index == 1):
                        kinder_0totnum = value.text
                    elif(index == 2):
                        kinder_1totnum = value.text
                    elif(index == 3):
                        kinder_2totnum = value.text
                    elif(index == 4):
                        kinder_3totnum = value.text
                    elif(index == 5):
                        kinder_4totnum = value.text
                    elif(index == 6):
                        kinder_5totnum = value.text
                    elif(index == 7):
                        kinder_mix1_totnum = value.text
                    elif(index == 8):
                        kinder_mix2_totnum = value.text
                    elif(index == 9):
                        kinder_sp_totnum = value.text
                    elif(index == 10):
                        kinder_aft_totnum = value.text
                    elif(index == 11):
                        kinder_etc_totnum = value.text
                    
                
                
                rows_totnum = tbody.find_elements_by_tag_name("tr")[2]
                body = rows_totnum.find_elements_by_tag_name("td")
                for index, value in enumerate(body):
                    if(index == 1):
                        kinder_0currnum = value.text 
                    elif(index == 2):
                        kinder_1currnum = value.text 
                    elif(index == 3):
                        kinder_2currnum = value.text 
                    elif(index == 4):
                        kinder_3currnum = value.text  
                    elif(index == 5):
                        kinder_4currnum = value.text 
                    elif(index == 6):
                        kinder_5currnum = value.text 
                    elif(index == 7):
                        kinder_mix1_currnum = value.text              
                    elif(index == 8):
                        kinder_mix2_currnum = value.text              
                    elif(index == 9):
                        kinder_sp_currnum = value.text                      
                    elif(index == 10):
                        kinder_aft_currnum = value.text                         
                    elif(index == 11):
                        kinder_etc_currnum = value.text     
                    
                # 총교직원 수(영유야 및 교직원 탭)
                teacher_num = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table:nth-child(6) > tbody > tr > td:nth-child(1)").text
                
                ## 교육 보육과정 탭 이동
                curriculum = driver.find_element_by_css_selector("#popWrap2 > div > div > ul > li:nth-child(4) > a")
                curriculum.click()
                

                ## 월마다 교육비용 업데이트       
                # 어린이집 보육료 현황
                etc_cost_tbl = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table:nth-child(6)")
                tbody = etc_cost_tbl.find_element_by_tag_name("tbody")
                cost_row = tbody.find_elements_by_tag_name("tr")[0]
                body = cost_row.find_elements_by_tag_name("td")
                for index, cost in enumerate(body):
                    if(index==0):
                        cost_0 = cost.text
                    elif(index==1):
                        cost_1 = cost.text
                    elif(index==2):
                        cost_2 = cost.text
                    elif(index==3):
                        cost_3 = cost.text
                    elif(index==4):
                        cost_4 = cost.text
                    elif(index==5):
                        cost_5 = cost.text   
                
                # 기타필요경비
                cost_dict = {}
                cost_table = driver.find_element_by_css_selector("#popWrap2 > div > div > div > table:nth-child(9)")
                tbody = cost_table.find_element_by_tag_name("tbody")
                cost_rows = tbody.find_elements_by_tag_name("tr")
                for index, value in enumerate(cost_rows):
                    detail = value.find_elements_by_tag_name("td")[1]
                    amt_money = value.find_elements_by_tag_name("td")[2]
                    pay_cycle = value.find_elements_by_tag_name("td")[3]

                    detail = detail.text+"("+pay_cycle.text+")"
                    pay_info = amt_money.text

                    cost_dict[detail] = pay_info

                
                # 테스트용 print문
                print("========================")
                print("기타필요경비")
                for key, val in cost_dict.items():
                    print(key, val)
                print("\n\n나이별 비용")
                print(cost_0, cost_1, cost_2, cost_3, cost_4, cost_5)
                print(kinder_name, kinder_chief, kinder_esta, kinder_admin, kinder_opertime) 
                print(kinder_call, kinder_addr, kinder_homep, teacher_num, kinder_totnum, kinder_currnum)
                print(kinder_0cls, kinder_0totnum, kinder_0currnum)
                print(kinder_1cls, kinder_1totnum, kinder_1currnum)
                print(kinder_2cls, kinder_2totnum, kinder_2currnum)
                print(kinder_3cls, kinder_3totnum, kinder_3currnum)
                print(kinder_4cls, kinder_4totnum, kinder_4currnum)
                print(kinder_5cls, kinder_5totnum, kinder_5currnum)
                print(kinder_mix1, kinder_mix1_totnum, kinder_mix1_currnum)
                print(kinder_mix2, kinder_mix2_totnum, kinder_mix2_currnum)
                print(kinder_spcls, kinder_sp_totnum, kinder_sp_currnum)
                print(kinder_after, kinder_aft_totnum, kinder_aft_currnum)
                print(kinder_etccls, kinder_etc_totnum, kinder_etc_currnum)
                print("========================")
                
                # 원래창으로 돌아옴
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            

                ## 유치원이름, 원장명, 설립유형, 관할 행정기관 ,전화번호, 홈페이지, 주소, 운영시간, 교사수, 총정원, 현인원, 학급별(학급수, 총정원, 현인원)
                # 비용회계 추가 (사이트 월단위 업데이트)
                kinder_doc = {
                    'kinder_name': kinder_name,
                    'kinder_chief' : kinder_chief,
                    'kinder_esta' : kinder_esta,
                    'kinder_admin' : kinder_admin,
                    'kinder_call' : kinder_call,
                    'kinder_homepage' : kinder_homep,
                    'kinder_address' : kinder_addr,
                    'kinder_opertime': kinder_opertime,
                    'kinder_teacher_num' : teacher_num,
                    'kinder_total_num' : kinder_totnum,
                    'kinder_current_num' : kinder_currnum,
                    'kinder_age_0': {'class' : kinder_0cls, 'total_num' : kinder_0totnum, 'current_num' : kinder_0currnum, 'care_fee' : cost_0},
                    'kinder_age_1': {'class' : kinder_1cls, 'total_num' : kinder_1totnum, 'current_num' : kinder_1currnum, 'care_fee' : cost_1},
                    'kinder_age_2': {'class' : kinder_2cls, 'total_num' : kinder_2totnum, 'current_num' : kinder_2currnum, 'care_fee' : cost_2},
                    'kinder_age_3': {'class' : kinder_3cls, 'total_num' : kinder_3totnum, 'current_num' : kinder_3currnum, 'care_fee' : cost_3},
                    'kinder_age_4': {'class' : kinder_4cls, 'total_num' : kinder_4totnum, 'current_num' : kinder_4currnum, 'care_fee' : cost_4},
                    'kinder_age_5': {'class' : kinder_5cls, 'total_num' : kinder_5totnum, 'current_num' : kinder_5currnum, 'care_fee' : cost_5},
                    'kinder_infant_mix' : {'class' : kinder_mix1, 'total_num' : kinder_mix1_totnum, 'current_num' : kinder_mix1_currnum},
                    'kinder_child_mix' : {'class' : kinder_mix2, 'total_num' : kinder_mix2_totnum, 'current_num' : kinder_mix2_currnum},
                    'kinder_special': {'class' : kinder_spcls, 'total_num' : kinder_sp_totnum, 'current_num' : kinder_sp_currnum},
                    'kinder_after' : {'class' : kinder_after, 'total_num' : kinder_aft_totnum, 'current_num' : kinder_aft_currnum},
                    'kinder_etc' : {'class' : kinder_etccls, 'total_num' : kinder_etc_totnum, 'current_num' : kinder_etc_currnum},
                    'kinder_etc_cost' : cost_dict ## 기타 경비                 
                }

                
                # db.kindergarden.insert_one(kinder_doc) # local
                cost_dict.clear()
                db.kinder(kinder_doc)

    
    
    
        

        