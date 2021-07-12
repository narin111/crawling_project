import scrapy
from selenium import webdriver
import pymongo

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbchildshcoolsite # local

# path = 'C:/Users/LG/Desktop/scrapy_prac/pagescrapy/chromedriver.exe'
path = 'D:/Desktop/crawling_project/childschool/chromedriver.exe'
driver = webdriver.Chrome(path)

# connection = pymongo.MongoClient("")
# db = connection.kinder_test

# clone test

class KinderSpider(scrapy.Spider):
    name = 'kinder'

    def start_requests(self):
        # pageCnt = 50
        yield scrapy.Request(url="https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?&pageCnt=10", callback=self.parse_allkinder)


    def parse_allkinder(self, response):
       
        # 마지막 페이지 번호 검사
        last_page = response.css('#resultArea > div.footer > div.paging > a.last::attr(href)').get()
        last_page = last_page.split("=")[1]
        print(int(last_page))

        # 페이지별로 parse_pagekinder 함수 호출
        # for i in ragne(1, last_page):
        for i in range(1, 2):
            page_url = 'https://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do?pageIndex={}&pageCnt=10'.format(i)
            yield scrapy.Request(url = page_url, callback = self.parse_pagekinder, meta={'page_kinder':page_url})
            

    # 페이지별 유치원 크롤링
    def parse_pagekinder(self, response):
       

        driver.get(response.meta['page_kinder'])
        kinder_listnum = driver.find_elements_by_css_selector("#resultArea > div.lists > ul > li")

        # for i in range(1, len(kinder_listnum)+1):
        for i in range(1, 3):
            
            driver.get(response.meta['page_kinder'])

            ####
            baby_or_kinder = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > span".format(i)).text
            ## 어린이집일 때는 크롤링x
            if(baby_or_kinder == "어"):
                print("어린이집")
                break 
            
            ## 유치원 크롤링
            elif(baby_or_kinder == "유"):
                print("유치원")      
                # 유치원/어린이집 클릭
                kinder_service = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > i".format(i)).text
                kinder_one = driver.find_element_by_css_selector("#resultArea > div.lists > ul > li:nth-child({}) > div.info > h5 > a".format(i))
                kinder_one.click()
                

                kinder_admin = driver.find_element_by_css_selector("#summaryBox > div > div.col.info > div.cont.base > ul > li:nth-child(7) > span").text

                

                    
                # 학급/교육 네비게이션 클릭
                kinder_class = driver.find_element_by_css_selector("#tabGroup > ul > li:nth-child(3) > a")
                kinder_class.click()

                kinder_name = driver.find_element_by_css_selector("#tabContTitle > i").text           
                
                # 총정원, 현인원, 학급 수, 학급 별 인원
                per_table = driver.find_element_by_css_selector("#subPage > div.wrap > div:nth-child(8) > table")
                tbody = per_table.find_element_by_tag_name("tbody")
                
                ## 테이블 구조 index가 row마다 다름
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
                        print("특수학급"+value.text+"\n\n") 


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

                # 비용, 회계 탭
                kinder_cost = driver.find_element_by_css_selector("#tabGroup > ul > li:nth-child(4) > a")
                kinder_cost.click()
                
                ### 교육과정 교육비용
                curriculum = driver.find_element_by_css_selector("#subPage > div > div:nth-child(11) > table")
                tbody = curriculum.find_element_by_tag_name("tbody")
                cost_rows = tbody.find_elements_by_tag_name("tr")

                # 기본경비 - 기본교육
                basic_age3 = {}; basic_age4 = {}; basic_age5 = {}
                # 선택경비 - 기본교육
                option_age3 = {}; option_age4 = {}; option_age5 = {}

                detail_flag = 0
                option_index = 0
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
                        
                        ## 간식비(월단위) : 10000원
                        detail_text = detail.text
                        detail = detail.text + "("+pay_cycle.text+")"
                        basic_age3[detail] = amt_money3.text
                        basic_age4[detail] = amt_money4.text
                        basic_age5[detail] = amt_money5.text

                        if(detail_text == "합계(월)"):
                            detail_flag = 1
                            continue
                            # print("detail_flag ==" + detail_flag)
                    
                    
                    elif(detail_flag == 1):
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
                
                # 방과후 과정 교육비용
                aft_curriculum = driver.find_element_by_css_selector("#subPage > div > div:nth-child(14) > table")
                tbody = aft_curriculum.find_element_by_tag_name("tbody")
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

                        if(detail_text == "합계(월)"):
                            detail_flag = 1 
                            continue
                            

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
                
                # 보건, 안전 탭
                kinder_safe = driver.find_element_by_css_selector("#tabGroup > ul > li:nth-child(5) > a")
                kinder_safe.click()

                # 안전교육 , 안전점검 버튼 클릭 \
                safety_btn = driver.find_element_by_css_selector("#tabMenus > ul > li:nth-child(2) > a")
                safety_btn.click()

                # 소방대피 훈련 여부
                kinder_fire =  driver.find_element_by_css_selector("#idPrint > div:nth-child(4) > table > tbody > tr > td:nth-child(2)").text
                fire_date = driver.find_element_by_css_selector("#idPrint > div:nth-child(4) > table > tbody > tr > td:nth-child(4)").text

                # 안전점검
                safety_check = {}
                safety_check["소방대피 훈련 여부"] = kinder_fire+"("+fire_date+")"
                safety_chk = driver.find_element_by_css_selector("#idPrint > div:nth-child(6) > table")
                chk_tbody = safety_chk.find_element_by_tag_name("tbody")
                
                tbody_rows = chk_tbody.find_elements_by_tag_name("tr")
                for index, value in enumerate(tbody_rows):
                    safety_item = value.find_elements_by_tag_name("th")[0].text
                    check_ox = value.find_elements_by_tag_name("td")[0].text
                    check_date = value.find_elements_by_tag_name("td")[1].text
                    safety_check[safety_item] = check_ox+"("+check_date+")"

                # 통학차량 운영여부
                kinder_bus = {}
                bus_num = driver.find_element_by_css_selector("#idPrint > div:nth-child(10) > table")
                bus_tbody = bus_num.find_element_by_tag_name("tbody")
                
                tbody_rows = bus_tbody.find_elements_by_tag_name("tr")
                for index, value in enumerate(tbody_rows):
                    kinder_bus["통학차량 운영여부"] = value.find_elements_by_tag_name("td")[0].text
                    kinder_bus["9인승 이상"] = value.find_elements_by_tag_name("td")[3].text
                    kinder_bus["12인승 이상"] = value.find_elements_by_tag_name("td")[4].text
                    kinder_bus["15인승 이상"] = value.find_elements_by_tag_name("td")[5].text
                    
                for key, val in kinder_bus.items():
                    print(key, val)
               
                # 유치원 이름, 관할행정기관, 유치원 총정원수/현원수, 교직원 수, 제공서비스, 학급별 인원수, 학급별 비용, 혼합반
                kinder_doc = {
                    "kinder_name" : kinder_name,
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
                        "after_option_cost" :aftoption_age5
                    },
                    
                    "kinder_mix_age34" : { "class" : kin34_class, "total_num" : kin34_totnum, "current_num" : kin34_currnum},
                    "kinder_mix_age45" : { "class" : kin45_class, "total_num" : kin45_totnum, "current_num" : kin45_currnum},
                    "kinder_mix_age35" : { "class" : kin35_class, "total_num" : kin35_totnum, "current_num" : kin35_currnum},
                    "kinder_special" : { "class" : kin_sp_class, "total_num" : kin_sp_totnum, "current_num" : kin_sp_currnum},

                    "kinder_safety"  : safety_check,
                    "kinder_bus" : kinder_bus


                }

                

                # db.kindergarden.insert_one(kinder_doc) # local
                # db.kinder.insert_one(kinder_doc) # epic_testdb

            basic_age3.clear()
            basic_age4.clear()
            basic_age5.clear()
            option_age3.clear()
            option_age4.clear()
            option_age5.clear()
            aftbasic_age3.clear()
            aftbasic_age4.clear()
            aftbasic_age5.clear()
            aftoption_age3.clear()
            aftoption_age4.clear()
            aftoption_age5.clear()
            safety_check.clear()
            kinder_bus.clear()
