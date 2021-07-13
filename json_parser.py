# from _typeshed import SupportsDivMod
### 한번에 작성
import json
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib.request
import requests
import time


with open('sidosgg.json', encoding='UTF8') as file:
    data = json.load(file)

# 기본현황 
basic = "https://e-childschoolinfo.moe.go.kr/api/notice/basicInfo.do"
# 직위.자격별 교직원현황 
teach = "https://e-childschoolinfo.moe.go.kr/api/notice/teachersInfo.do"
# 수업일수 현황 
teach_days = "https://e-childschoolinfo.moe.go.kr/api/notice/lessonDay.do"
# 급식운영현황 
meal = "https://e-childschoolinfo.moe.go.kr/api/notice/schoolMeal.do"
# 통학차량현황 
bus = "https://e-childschoolinfo.moe.go.kr/api/notice/schoolBus.do"
# 근속연수 현황 
work_year = "https://e-childschoolinfo.moe.go.kr/api/notice/yearOfWork.do"
# 환경위생 관리현황 
enviro = "https://e-childschoolinfo.moe.go.kr/api/notice/environmentHygiene.do"
# 안전점검, 교육 실시현황 
safety = "https://e-childschoolinfo.moe.go.kr/api/notice/safetyEdu.do"
# 공제회 가입 현황 
deduc = "https://e-childschoolinfo.moe.go.kr/api/notice/deductionSociety.do"
# 보험별 가입 현황 
insur = "https://e-childschoolinfo.moe.go.kr/api/notice/insurance.do"

apikey = "2039b8c5db3c4385b39b00ae74b783cc"

for one in data: # sidosgg.json 추출
    time.sleep(0.5)
    sidoCode = one['시도코드']
    sggCode = one['시군구코드']
    print("==============")
    print(sidoCode, sggCode)
    print("==============")
    query = '?' + "key=" + apikey + "&sidoCode=" + str(sidoCode) + "&sggCode=" + str(sggCode)
    
    url = basic
    req = urllib.request.urlopen(url+query)
    res = req.readline()
    j = json.loads(res)
    jarr_basic = j.get("kinderInfo")


    req_teach = urllib.request.urlopen(teach+query)
    res_teach = req_teach.readline()
    j_teach = json.loads(res_teach)
    jarr_teach = j_teach.get("kinderInfo")
  

    print(jarr_basic[1].get("kindername"))
    print(type(len(jarr_basic)))
    
    if(len(jarr_basic) != 0):
        for i in range(0, len(jarr_basic)):
            kindername = jarr_basic[i].get("kindername")
            officeedu = jarr_basic[i].get("officeedu") # 교육청명
            subofficeedu = jarr_basic[i].get("subofficeedu") # 교육지원청명
            kinderCode = jarr_basic[i].get("kinderCode") # 유치원코드
            establish = jarr_basic[i].get("establish") # 설립유형
            rppname = jarr_basic[i].get("rppnname") # 대표자명
            ldgrname = jarr_basic[i].get("ldgrname") # 원장명
            edate = jarr_basic[i].get("edate") # 설립일
            odate = jarr_basic[i].get("odate") # 개원일
            addr = jarr_basic[i].get("addr") # 주소
            telno = jarr_basic[i].get("telno") # 전화번호
            hpaddr = jarr_basic[i].get("hpaddr") # 홈페이지
            opertime = jarr_basic[i].get("opertime") # 운영시간
            clcnt3 = jarr_basic[i].get("clcnt3") # 만 3세 학급수
            clcnt4 = jarr_basic[i].get("clcnt4") # 만 4세 학급수
            clcnt5 = jarr_basic[i].get("clcnt5") # 만 5세 학급수
            mixppcnt = jarr_basic[i].get("mixppcnt") # 혼합유아수
            shppcnt = jarr_basic[i].get("shppcnt") # 특수유아수
            pbnttmng = jarr_basic[i].get("pbnttmng") # 공시차수

            drcnt = jarr_teach[i].get("drcnt") # 원장수
            adcnt = jarr_teach[i].get("adcnt") # 원감수
            hdst_thcnt = jarr_teach[i].get("hdst_thcnt") # 수석교사수
            asps_thcnt = jarr_teach[i].get("asps_thcnt") # 보직교사수
            gnrl_thcnt = jarr_teach[i].get("gnrl_thcnt") # 일반교사수
            spcn_thcnt = jarr_teach[i].get("spcn_thcnt") # 특수교사수
            ntcnt = jarr_teach[i].get("ntcnt") # 보건교사수
            ntrt_thcnt = jarr_teach[i].get("ntrt_thcnt") # 영양교사수
            shcnt_thcnt = jarr_teach[i].get("shcnt_thcnt") #기간제교사수
            incnt = jarr_teach[i].get("incnt") # 강사수
            owcnt = jarr_teach[i].get("owcnt") # 사무직원수
            hdst_tchr_qacnt = jarr_teach[i].get("hdst_tchr_qacnt") # 수석교사자격수
            rgth_gd1_qacnt = jarr_teach[i].get("rgth_gd1_qacnt") # 공정교사1급자격수
            rgth_gd2_qacnt = jarr_teach[i].get("rgth_gd2_qacnt") # 정교사2급자격수
            asth_qacnt = jarr_teach[i].get("asth_qacnt") # 준교사 자격수
            pbntTmng = jarr_teach[i].get("pbntTmng") # 공시차수


            
            
            print(kindername, officeedu, subofficeedu, kinderCode, establish, rppname, ldgrname, edate, odate, addr, telno, hpaddr, opertime)
            print(clcnt3, clcnt4, clcnt5, mixppcnt, shppcnt)
            print(drcnt, adcnt, hdst_thcnt, asps_thcnt)

           

 
    # kinderList = requests.get(url+query).json()
    # kinders = kinderList["kinderInfo"]
    
    
    




    # print(sidoCode, sggCode)




# ' '






