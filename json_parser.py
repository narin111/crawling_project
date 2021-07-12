import json
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib.request
import requests


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
    sidoCode = one['시도코드']
    sggCode = one['시군구코드']
    
    # queryParams = '?' + urlencode({ quote_plus('key') : '2039b8c5db3c4385b39b00ae74b783cc', quote_plus('sidoCode') : str(sidoCode) , quote_plus('sggCode') : str(sggCode) })
    query = '?' + "key=" + apikey + "&sidoCode=" + str(sidoCode) + "&sggCode=" + str(sggCode)
    
    url = basic
    """
    req = urllib.request.urlopen(url+queryParams)
    res = req.readline()
    
    j = json.loads(res)
    print(sidoCode, sggCode)
    
    # print(j["kinderInfo"][1]["kindername"])
    jarr = j.get("kinderInfo")
    for list in jarr:
        
        print(list.get("kindername"))
    """
    kinderlist = requests.get(url+query)
    




    # print(sidoCode, sggCode)



#건물현황 https://e-childschoolinfo.moe.go.kr/api/notice/building.do
#교실면적현황 https://e-childschoolinfo.moe.go.kr/api/notice/classArea.do

'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'






