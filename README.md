# crawling_project
- 유치원 크롤링(childschool)
- 어린이집 크롤링(kindergarten)


### sidosgg.json 
 
> https://e-childschoolinfo.moe.go.kr/openApi/sidoSigunguCode.do  <- 엑셀파일 다운     
> 엑셀파일 출처: 유치원알리미 사이트 - https://e-childschoolinfo.moe.go.kr/openApi/openApiList.do
 - 시도시군구코드 엑셀파일 -> json 변환
 - http://shancarter.github.io/mr-data-converter/ (json format 변환)
 - https://jsonformatter.curiousconcept.com/ (json 형태 파일 다운로드)
 - 2021.07.29 목요일 json 파일 Github 추가


### childschool
유치원 크롤링 project
- kinder02.py 가 최신 python 파일


### kindergarten
어린이집 크롤링 project
- kind02.py 가 최신 python 파일


### json_separate_field10.py
- 유치원 API parsing python file
- 유치원 스크래핑 DB collection과 같은 collection에 들어감 (같은 유치원에 api 데이터 upsert)
