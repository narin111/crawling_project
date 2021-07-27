import scrapy
from pymongo.message import update
from pymongo.operations import UpdateOne, UpdateMany
import scrapy
from selenium import webdriver
import pymongo
import time
from pymongo import InsertOne 

#### spider quit and functioncall
from scrapy import signals
from pydispatch import dispatcher
####

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbchildshcoolsite # local

# path = 'C:/Users/LG/Desktop/현장실습/chromedriver.exe'
path = 'D:/Desktop/crawling_project/childschool/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
driver = webdriver.Chrome(path, options=options)




class Kinder02Spider(scrapy.Spider):
    name = 'kinder02'
    
    ## spider가 종료되면 데이터베이스 updated: 0 인 것 삭제
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def spider_closed(self, spider):
        print("spider closed")
        db.kinder_test.delete_many({ "updated" : 0 })
    
    
    # spider 시작 url
    def start_requests(self):
        yield scrapy.Request(url="https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?&pageCnt=50", callback=self.parse_allkinder)


    def parse_allkinder(self, response):
        
        ## 크롤링 시작 전 db의 모든 doc updated = 0 으로 초기화
        db.kinder_test.update_many(
            { "kinderall" : 1 },
            { '$set' : { "updated" : 0 }}
        )

       
        # 유치원 목록 마지막 페이지 번호 가져오기
        last_page = response.css('#resultArea > div.footer > div.paging > a.last::attr(href)').get()
        last_page = last_page.split("=")[1]
        print(int(last_page))

        
        # 페이지마다 parse_pagekinder 함수 호출
        for i in range(1, int(last_page)+1):
        # for i in range(29, 30):
            page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=50'.format(i)
            
            driver.get(page_url)
            
            time.sleep(0.3)

            # 페이지 당 유치원 목록 개수
            kinder_listnum = driver.find_elements_by_css_selector("#resultArea > div.lists > ul > li")
            
            print(len(kinder_listnum))
            
            bulk_list = []

            
            for i in range(1, len(kinder_listnum)+1):
            # for i in range(1, 5):
                
                # 유치원/어린이집 옆에 "유" 또는 "어" 표시가 있음
                baby_or_kinder = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > span".format(i)).text

                ## 어린이집일 때는 크롤링x
                if(baby_or_kinder == "어"): 
                    continue
                
                ## 유치원 크롤링
                elif(baby_or_kinder == "유"):
                    

                    """
                    1. 폐원, 휴원한 유치원이라면 
                    2. continue
                    """
                    try:
                        kinder_closed = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > span.est.closed".format(i)).text
                        if(kinder_closed == "폐원"):
                            continue
                    except:
                        kinder_closed = "-"

                    try:
                        kinder_closed = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > span.est.rested".format(i)).text
                        if(kinder_closed == "휴원"):
                            continue
                    except:
                        kinder_closed = "-"
                        
                    # 유치원/어린이집 클릭
                    kinder_service = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > i".format(i)).text
                    kinder_one = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > a".format(i))
                    kinder_one.click()



                    """
                    1. 유치원 목록에 유치원이 있지만 해당 유치원에서 정보게시를 하지 않았으면 
                    2. alert창이 뜸 -> dismiss하고 뒤로가기해서 목록페이지로 돌아감
                    3. continue
                    """
                    try:
                        noinfo_alert = driver.switch_to_alert()
                        noinfo_alert.dismiss()
                        driver.back()
                        continue
                    
                    except:
                        
                        """
                        폐원, 휴원 하지않고 정보 제대로 올렸을 경우
                        유치원 크롤링 시작
                        """

                        # 대표자명, 원장명, 관할행정기관
                        kinder_rppnname = driver.find_element_by_css_selector("#summaryBox > div > div.col.info > div.cont.base > ul > li:nth-child(3) > span").text
                        kinder_ldgrname = driver.find_element_by_css_selector("#summaryBox > div > div.col.info > div.cont.base > ul > li:nth-child(4) > span").text
                        kinder_admin = driver.find_element_by_css_selector("#summaryBox > div > div.col.info > div.cont.base > ul > li:nth-child(7) > span").text  
                        

                        # 학급/교육 탭으로 넘어감
                        kinder_class = driver.find_element_by_css_selector("#tabGroup > ul > li:nth-child(3) > a")
                        kinder_class.click()

                        kinder_name = driver.find_element_by_css_selector("#tabContTitle > i").text           
                        
                        # 총정원, 현인원, 학급 수, 학급 별 인원 크롤링
                        per_table = driver.find_element_by_css_selector("#subPage > div.wrap > div:nth-child(8) > table")
                        tbody = per_table.find_element_by_tag_name("tbody")
                        rows_class = tbody.find_elements_by_tag_name("tr")[0]
                        body = rows_class.find_elements_by_tag_name("td")
                        for index, value in enumerate(body):
                            if(index == 0):
                                kin_totnum = value.text
                            elif(index == 1):
                                kin_currnum = value.text
                            elif(index == 2):
                                kin3_class = value.text
                            elif(index == 3):
                                kin4_class = value.text
                            elif(index == 4):
                                kin5_class = value.text
                            elif(index == 5):
                                kin34_class = value.text 
                            elif(index == 6):
                                kin45_class = value.text
                            elif(index == 7):
                                kin35_class = value.text
                            elif(index == 8):
                                kin_sp_class = value.text 

                        
                        rows_totnum = tbody.find_elements_by_tag_name("tr")[1]
                        body = rows_totnum.find_elements_by_tag_name("td")
                        for index, value in enumerate(body):
                            if(index == 0):
                                kin3_totnum = value.text
                            elif(index == 1):
                                kin4_totnum = value.text
                            elif(index == 2):
                                kin5_totnum = value.text
                            elif(index == 3):
                                kin34_totnum = value.text 
                            elif(index == 4):
                                kin45_totnum = value.text
                            elif(index == 5):
                                kin35_totnum = value.text
                            elif(index == 6):
                                kin_sp_totnum = value.text
                                


                        rows_currnum = tbody.find_elements_by_tag_name("tr")[1]
                        body = rows_currnum.find_elements_by_tag_name("td")
                        for index, value in enumerate(body):
                            if(index == 0):
                                kin3_currnum = value.text
                            elif(index == 1):
                                kin4_currnum = value.text
                            elif(index == 2):
                                kin5_currnum = value.text
                            elif(index == 3):
                                kin34_currnum = value.text
                            elif(index == 4):
                                kin45_currnum = value.text
                            elif(index == 5):
                                kin35_currnum = value.text
                            elif(index == 6):
                                kin_sp_currnum = value.text
                            
                        # 교직원 수
                        teachernum = driver.find_element_by_css_selector("#subPage > div.wrap > div:nth-child(11) > table > tbody > tr > td:nth-child(1)").text

                        # 비용, 회계 탭으로 넘어감
                        kinder_cost = driver.find_element_by_css_selector("#tabGroup > ul > li:nth-child(4) > a")
                        kinder_cost.click()
                        
                        # 공시차수
                        update_time = driver.find_element_by_css_selector("#select-time_displayAtag").text
                        # print(update_time)
                        

                        
                        # 기본경비 - 기본교육
                        basic_age3 = {}; basic_age4 = {}; basic_age5 = {}
                        # 선택경비 - 기본교육
                        option_age3 = {}; option_age4 = {}; option_age5 = {}

                        detail_flag = 0
                        option_index = 0

                        # 기본교육 비용 표 크롤링
                        """
                        기본경비와 선택경비가 한 테이블안에 들어가있어 구별어려움
                        기본경비 항목 중 마지막 행에 "합계"라는 글자를 기준으로 기본경비, 선택경비로 나뉨
                        """
                        tbody = driver.find_element_by_css_selector("#subPage > div > div:nth-child(11) > table > tbody")
                        cost_rows = tbody.find_elements_by_tag_name("tr")
                        for index, value in enumerate(cost_rows):
                            if(detail_flag == 0):
                                if(index==0):
                                    detail = value.find_elements_by_tag_name("th")[1]
                                elif(index!=0):
                                    detail = value.find_elements_by_tag_name("th")[0]
                                amt_money3 = value.find_elements_by_tag_name("td")[0]
                                amt_money4 = value.find_elements_by_tag_name("td")[1]
                                amt_money5 = value.find_elements_by_tag_name("td")[2]
                                pay_cycle = value.find_elements_by_tag_name("td")[3]
                                
                                ## ex) 간식비(월단위) : 10000원
                                detail_text = detail.text
                                detail = detail.text + "("+pay_cycle.text+")"
                                basic_age3[detail] = amt_money3.text
                                basic_age4[detail] = amt_money4.text
                                basic_age5[detail] = amt_money5.text

                                if(detail_text == "합계(월)"):
                                    detail_flag = 1
                                    continue
                                    
                            
                            
                            elif(detail_flag == 1):
                                # 선택경비의 첫 항목은 th[1]에 있음 나머지는 th[0]에 있음
                                # 항목(입학금, 원복비, 현장학습비 등)
                                # option_index로 구분
                                if(option_index == 0):
                                    detail = value.find_elements_by_tag_name("th")[1]
                                elif(option_index != 0):
                                    detail = value.find_elements_by_tag_name("th")[0]

                                amt_money3 = value.find_elements_by_tag_name("td")[0]
                                amt_money4 = value.find_elements_by_tag_name("td")[1]
                                amt_money5 = value.find_elements_by_tag_name("td")[2]
                                pay_cycle = value.find_elements_by_tag_name("td")[3]
                                
                                ## 간식비(월단위) : 10000원
                                detail = detail.text +"("+pay_cycle.text+")"
                                option_age3[detail] = amt_money3.text  
                                option_age4[detail] = amt_money4.text
                                option_age5[detail] = amt_money5.text
                                
                                option_index += 1
                        

                        # 기본과정 비용 크롤링방법과 동일
                        # 방과후과정 표 크롤링
                        tbody = driver.find_element_by_css_selector("#subPage > div > div:nth-child(14) > table > tbody")
                        cost_rows = tbody.find_elements_by_tag_name("tr")

                        # 기본경비 - 방과후
                        aftbasic_age3 = {}; aftbasic_age4 = {}; aftbasic_age5 = {}
                        # 선택경비 - 방과후
                        aftoption_age3 = {}; aftoption_age4 = {}; aftoption_age5 = {}

                        detail_flag = 0
                        option_index = 0
                        for index, value in enumerate(cost_rows):
                            if(detail_flag == 0):
                                if(index==0):
                                    detail = value.find_elements_by_tag_name("th")[1]
                                if(index!=0):
                                    detail = value.find_elements_by_tag_name("th")[0]
                                amt_money3 = value.find_elements_by_tag_name("td")[0]
                                amt_money4 = value.find_elements_by_tag_name("td")[1]
                                amt_money5 = value.find_elements_by_tag_name("td")[2]
                                pay_cycle = value.find_elements_by_tag_name("td")[3]
                                
                                detail_text = detail.text
                                detail = detail.text + "("+pay_cycle.text+")"
                                aftbasic_age3[detail] = amt_money3.text
                                aftbasic_age4[detail] = amt_money4.text
                                aftbasic_age5[detail] = amt_money5.text

                                
                                """
                                테이블 값 중 합계(월)이 나오면
                                그 아래 행부터는 선택경비
                                detail_flag = 1 
                                for문에서 현재 테이블 row 위치가 기본경비인지 선택경비인지 구분
                                """
                                if(detail_text == "합계(월)"):
                                    detail_flag = 1 
                                    continue
                                    

                            # 선택경비 크롤링
                            # 선택경비에서 첫번째 행만 항목이 th[1]에 있고 나머지는 모두 th[0]           
                            elif(detail_flag == 1):
                                if(option_index==0):
                                    detail = value.find_elements_by_tag_name("th")[1]
                                elif(option_index != 0):
                                    detail = value.find_elements_by_tag_name("th")[0] 
                                amt_money3 = value.find_elements_by_tag_name("td")[0]
                                amt_money4 = value.find_elements_by_tag_name("td")[1]
                                amt_money5 = value.find_elements_by_tag_name("td")[2]
                                pay_cycle = value.find_elements_by_tag_name("td")[3]
                                
                                detail = detail.text + "("+pay_cycle.text+")"
                                aftoption_age3[detail] = amt_money3.text  
                                aftoption_age4[detail] = amt_money4.text
                                aftoption_age5[detail] = amt_money5.text
                                
                                option_index += 1
                        
                    

                        driver.back()
                        driver.back()
                        driver.back()
                        

                        # 유치원 이름, 대표자명, 원장명, 관할행정기관, 유치원 총정원수/현원수, 교직원 수, 제공서비스, 학급별 인원수, 학급별 비용, 혼합반
                        kinder_doc = {
                            "update_time" : update_time,
                            "kindername" : kinder_name,
                            "rppnname" : kinder_rppnname,
                            "ldgrname" : kinder_ldgrname,
                            "kinder_admin" : kinder_admin,
                            "kinder_total_num" : kin_totnum,
                            "kinder_current_num" : kin_currnum,
                            "kinder_teacher_num" : teachernum,
                            "kinder_service" : kinder_service,
                            "kinder_age3" : {   
                                "class" : kin3_class,
                                "total_num" : kin3_totnum,
                                "current_num" : kin3_currnum,
                                "basic_cost" : basic_age3, 
                                "option_cost" : option_age3,
                                "after_basic_cost" : aftbasic_age3,
                                "after_option_cost" : aftoption_age3
                            },
                            "kinder_age4" : {
                                "class" : kin4_class,
                                "total_num" : kin4_totnum,
                                "current_num" : kin4_currnum, 
                                "basic_cost" : basic_age4,
                                "option_cost" : option_age4,
                                "after_basic_cost" : aftbasic_age4,
                                "after_option_cost" :aftoption_age4
                            },
                            "kinder_age5" : {
                                "class" : kin5_class,
                                "total_num" : kin5_totnum,
                                "current_num" : kin5_currnum, 
                                "basic_cost" : basic_age5,
                                "option_cost" : option_age5,
                                "after_basic_cost" : aftbasic_age5,
                                "after_option_cost" : aftoption_age5
                            },
                            
                            "kinder_mix_age34" : { "class" : kin34_class, "total_num" : kin34_totnum, "current_num" : kin34_currnum},
                            "kinder_mix_age45" : { "class" : kin45_class, "total_num" : kin45_totnum, "current_num" : kin45_currnum},
                            "kinder_mix_age35" : { "class" : kin35_class, "total_num" : kin35_totnum, "current_num" : kin35_currnum},
                            "kinder_special" : { "class" : kin_sp_class, "total_num" : kin_sp_totnum, "current_num" : kin_sp_currnum},
                        
                        
                            "kinderall" : 1 ,
                            "updated" : 1
                            

                        } 
                        
                        print(kinder_name)
                        

                        # upsert 사용하기 
                        # 같은 이름 유치원인 경우를 구별하기위해 kinder_admin도 추가
                        bulk_list.append(UpdateOne({"kinder_name": kinder_name, 
                                                    "kinder_admin" : kinder_admin}, {'$set' : kinder_doc }, upsert=True ))
                        
                        
                    
                    
            # bulk_list에 값이 들어가있을 때만 db write
            if bulk_list:
                db.kinder_test.bulk_write(bulk_list)

            # db.kinder.bulk_write(bulk_list) # epic_testdb
            
