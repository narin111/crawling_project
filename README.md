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


### json_separate_field10.py
- 유치원 API parsing python file
- 유치원 스크래핑 DB collection과 같은 collection에 들어감 (같은 유치원에 api 데이터 upsert)


### childschool
유치원 크롤링 project
- kinder02.py 가 최신 python 파일
<img src = "https://user-images.githubusercontent.com/43459698/127446757-e9c075e5-948f-495b-84f4-b7321bf13ae0.png" width="80%" height = "80%">
<img src = "https://user-images.githubusercontent.com/43459698/127446877-795672cd-917d-4f81-80d4-50ac24b7c161.png" width="80%" height = "80%">



### kindergarten
어린이집 크롤링 project
- kind02.py 가 최신 python 파일
<img src = "https://user-images.githubusercontent.com/43459698/127446940-5c024ac9-37d4-4f59-83e0-364639d5daaa.png" width="80%" height = "80%">
<img src = "https://user-images.githubusercontent.com/43459698/127447005-da5b6853-8af6-4666-8144-5c6c112a27a8.png" width="80%" height = "80%">


