import scrapy
import enum
import scrapy
from selenium import webdriver
import time
import pymongo
from pymongo.operations import UpdateOne

from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
from pydispatch import dispatcher

from selenium.common.exceptions import UnexpectedAlertPresentException


# path = 'C:/Users/LG/Desktop/child_field/kindergarten/chromedriver.exe'
path = 'D:/Desktop/crawling_project/childschool/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(path, options=options)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbchildshcoolsite # local



class Kind02Spider(scrapy.Spider):
    name = 'kind02'
    
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def spider_closed(self, spider):
        print("spider closed")
        db.eorini_test_1.delete_many({ "updated" : 0 })
 
    def start_requests(self):
        # pageCnt = 50 or 10
        yield scrapy.Request(url="https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageCnt=50", callback=self.parse_childpage)
       

    def parse_childpage(self, response):

        ## 크롤링 시작 전 db의 모든 doc updated = 0 으로 초기화
        db.eorini_test_1.update_many(
            { 'kinderall' : 1 },
            { '$set' : { 'updated' : 0 }}
        )

        last_page = response.css('#resultArea > div.footer > div.paging > a.last::attr(href)').get()
        last_page = last_page.split("=")[1]
        
        
        for i in range(int(last_page), 0, -1): # (lstpg, 0, -1)
        # for i in range(210, 211):
            page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=50'.format(i) 
           
            driver.get(page_url)

            print(page_url)
         
            # 페이지에서 유치원/어린이집 리스트 개수 
            kinder_list = driver.find_elements_by_css_selector("#resultArea > div.lists > ul > li")
            
            cost_dict = {}
            bulk_list = []
            # for i in range(1, 3):
            for i in range(1, len(kinder_list)+1):
                
                baby_or_kinder = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > span".format(i)).text
                

                # 유치원일때 InvalidOperation: No operations to execute 오류
                if(baby_or_kinder == "유"):
                    continue

                elif(baby_or_kinder == "어"):
                
                
                    kinder_one = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > a".format(i))
                    kinder_one.click()

                    # 활성탭 바꿈
                    driver.switch_to.window(driver.window_handles[-1])

                    # 바뀐 활성탭에서 alert창 처리해야함
                    # 폐원된 시설 예외처리
                    


                    # No such alert 오류 처리
                    try: 
                        # 폐지된 시설 .... alert 처리
                        alert = driver.switch_to_alert()
                        print(alert.text)
                        alert.dismiss()

                        # 해당 어린이집 활성탭 닫고 다시 어린이집 목록으로
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue
                    

                    # 크롤링 시작 
                    # 110 ~ 255
                    except:                       
                        time.sleep(0.3)
          
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

                        # 어린이집 인원 수 크롤링
                        # 130 ~ 212
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
                            

                        # 총교직원 수(영유아 및 교직원 탭)
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

                        
                        # 1. 어린이집 정보 활성탭 닫고
                        # 2. 원래창으로 돌아옴
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])


                        print(kinder_name)
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
                            'kinder_etc_cost' : cost_dict,
                            
                            'kinderall' : 1, # update 해주기위한 기본field
                            'updated' : 1                 
                        }

                        
                        bulk_list.append(UpdateOne({"kinder_name": kinder_name, 
                                                    "kinder_admin" : kinder_admin}, {'$set' : kinder_doc}, upsert=True ))
                    

                    
            

            # 리스트에 비었을 때 InvalidOperation: No operations to execute 오류
            # 리스트에 값 들어있을 때만 db write
            if bulk_list:
                db.eorini_test_1.bulk_write(bulk_list)
            
            cost_dict.clear()
        
        
        
            

            
