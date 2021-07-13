# from _typeshed import SupportsDivMod
import json
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib.request
import requests
import time

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbkinderapi # local




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

    kinder_list = []
    
    # 기본현황
    url = basic
    req = urllib.request.urlopen(url+query)
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        establish = list.get("establish") # 설립유형
        rppname = list.get("rppnname") # 대표자명
        ldgrname = list.get("ldgrname") # 원장명
        edate = list.get("edate") # 설립일
        odate = list.get("odate") # 개원일
        addr = list.get("addr") # 주소
        telno = list.get("telno") # 전화번호
        hpaddr = list.get("hpaddr") # 홈페이지
        opertime = list.get("opertime") # 운영시간
        clcnt3 = list.get("clcnt3") # 만 3세 학급수
        clcnt4 = list.get("clcnt4") # 만 4세 학급수
        clcnt5 = list.get("clcnt5") # 만 5세 학급수
        mixppcnt = list.get("mixppcnt") # 혼합유아수
        shppcnt = list.get("shppcnt") # 특수유아수
        pbnttmng = list.get("pbnttmng") # 공시차수
        #
        # basic_doc = {
        #     "kindername" : list.get("kindername")
        # }
        basic_doc = {
            "kindername" : kindername,
            "officeedu" : officeedu,
            "subofficedu" : subofficeedu,
            "kinderCode" : kinderCode,
            "establish" : establish,
            "rppname" : rppname,
            "ldgrname" : ldgrname,
            "edate" : edate,
            "odate" : odate,
            "addr" : addr,
            "telno" : telno,
            "hpaddr" : hpaddr,
            "opertime" : opertime,
            "clcnt3" : clcnt3,
            "clcnt4" : clcnt4,
            "clcnt5" : clcnt5,
            "mixppcnt" : mixppcnt,
            "shppcnt" : shppcnt,
            "pbnttmng" : pbnttmng
        }

        # db.kinder_basic.insert_one(basic_doc)  # bulk write(insertOne)로 수정하기
        #  
        kinder_list.append(basic_doc)
    
    # 직위 자격별 교직원현황
    # 딕셔너리 list에서 kinderCode가 같은 딕셔너리와 딕셔너리 합치기
    req = urllib.request.urlopen(teach+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        establish = list.get("establish") # 설립유형
        drcnt = list.get("drcnt") # 원장수
        adcnt = list.get("adcnt") # 원감수
        hdst_thcnt = list.get("hdst_thcnt") # 수석교사수
        asps_thcnt = list.get("asps_thcnt") # 보직교사수
        gnrl_thcnt = list.get("gnrl_thcnt") # 일반교사수
        spcn_thcnt = list.get("spcn_thcnt") # 특수교사수
        ntcnt = list.get("ntcnt") # 보건교사수
        ntrt_thcnt = list.get("ntrt_thcnt") # 영양교사수
        shcnt_thcnt = list.get("shcnt_thcnt") #기간제교사수
        incnt = list.get("incnt") # 강사수
        owcnt = list.get("owcnt") # 사무직원수
        hdst_tchr_qacnt = list.get("hdst_tchr_qacnt") # 수석교사자격수
        rgth_gd1_qacnt = list.get("rgth_gd1_qacnt") # 공정교사1급자격수
        rgth_gd2_qacnt = list.get("rgth_gd2_qacnt") # 정교사2급자격수
        asth_qacnt = list.get("asth_qacnt") # 준교사 자격수
        pbntTmng = list.get("pbntTmng") # 공시차수

        #
        teach_doc = {
            "drcnt" : drcnt,
            "adcnt" : adcnt,
            "hdst_thcnt" : hdst_thcnt,
            "asps_thcnt" : asps_thcnt,
            "gnrl_thcnt" : gnrl_thcnt,
            "spcn_thcnt" : spcn_thcnt,
            "ntcnt" : ntcnt,
            "ntrt_thcnt" : ntrt_thcnt,
            "shcnt_thcnt" : shcnt_thcnt,
            "incnt" : incnt,
            "owcnt" : owcnt,
            "hdst_tchr_qacnt" : hdst_tchr_qacnt,
            "rgth_gd1_qacnt" : rgth_gd1_qacnt,
            "rgth_gd2_qacnt" : rgth_gd2_qacnt,
            "asth_qacnt" : asth_qacnt,
            "pbntTmng" : pbntTmng
        }

        Codesame = (item for item in kinder_list if['kinderCode'] == kinderCode) # kinder_list에서 kinderCode가 같은 유치원에 딕셔너리 합침
        
        

        # db.kinder_teach.insert_one(teach_doc)
        # 


    # 수업일수 현황
    req = urllib.request.urlopen(teach+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        establish = list.get("establish") # 설립유형
        ag3_lsn_dcnt = list.get("ag3_lsn_dcnt")
        ag4_lsn_dcnt = list.get("ag4_lsn_dcnt")
        ag5_lsn_dcnt = list.get("ag5_lsn_dcnt")
        mix_age_lsn_dcnt = list.get("mix_age_lsn_dcnt")
        spcl_lsn_dcnt = list.get("spcl_lsn_dcnt")
        afsc_pros_lsn_dcnt = list.get("afsc_pros_lsn_dcnt")
        ldnum_blw_yn = list.get("ldnum_blw_yn")
        fdtn_kndr_yn = list.get("fdtn_kndr_yn")
        pbntTmng = list.get("pbntTmng")



    # 급식운영현황
    req = urllib.request.urlopen(meal+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        establish = list.get("establish") # 설립유형
        mlsr_oprn_way_tp_cd = list.get("mlsr_oprn_way_tp_cd") 
        cons_ents_nm = list.get("cons_ents_nm")
        al_kpcnt = list.get("al_kpcnt")
        mlsr_kpcnt = list.get("mlsr_kpcnt")
        ntrt_tchr_agmt_yn = list.get("ntrt_tchr_agmt_yn")
        snge_agmt_ntrt_thcnt = list.get("snge_agmt_ntrt_thcnt")
        cprt_agmt_ntrt_thcnt = list.get("cprt_agmt_ntrt_thcnt")
        ckcnt = list.get("ckcnt")
        cmcnt = list.get("cmcnt")
        mas_mspl_dclr_yn = list.get("mas_mspl_dclr_yn")
        pbntTmng = list.get("pbntTmng")



    # 통학차량운영
    req = urllib.request.urlopen(bus+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        establish = list.get("establish") # 설립유형
        vhcl_oprn_yn = list.get("vhcl_oprn_yn") 
        opra_vhcnt = list.get("opra_vhcnt")
        dclr_vhcnt = list.get("dclr_vhcnt")
        psg9_dclr_vhcnt = list.get("psg9_dclr_vhcnt")
        psg12_dclr_vhcnt = list.get("psg12_dclr_vhcnt")
        psg15_dclr_vhcnt = list.get("psg15_dclr_vhcnt")
        pbntTmng = list.get("pbntTmng")

    
    # 근속연수운영
    req = urllib.request.urlopen(work_year+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        estb_pt = list.get("estb_pt") # 설립유형
        yy1_undr_thcnt = list.get("yy1_undr_thcnt")
        yy1_abv_yy2_undr_thcnt = list.get("yy1_abv_yy2_undr_thcnt")
        yy2_abv_yy4_undr_thcnt = list.get("yy2_abv_yy4_undr_thcnt")
        yy4_abv_yy6_undr_thcnt = list.get("yy4_abv_yy6_undr_thcnt")
        yy6_abv_thcnt = list.get("yy6_abv_thcnt")
        pbntTmng = list.get("pbntTmng")

    
    # 환경위생관리
    req = urllib.request.urlopen(enviro+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        estb_pt = list.get("estb_pt") # 설립유형
        arql_chk_dt = list.get("arql_chk_dt")
        arql_chk_rslt_tp_cd = list.get("arql_chk_rslt_tp_cd")
        fxtm_dsnf_trgt_yn = list.get("fxtm_dsnf_trgt_yn")
        fxtm_dsnf_chk_dt = list.get("fxtm_dsnf_chk_dt")
        fxtm_dsnf_chk_rslt_tp_cd = list.get("fxtm_dsnf_chk_rslt_tp_cd")
        tp_01 = list.get("tp_01")
        tp_02 = list.get("tp_02")
        tp_03 = list.get("tp_03")
        tp_04 = list.get("tp_04")
        unwt_qlwt_insc_yn = list.get("unwt_qlwt_insc_yn")
        qlwt_insc_dt = list.get("qlwt_insc_dt")
        qlwt_insc_stby_yn = list.get("qlwt_insc_stby_yn")
        mdst_chk_dt = list.get("mdst_chk_dt")
        mdst_chk_rslt_cd = list.get("mdst_chk_rslt_cd")
        ilmn_chk_dt = list.get("ilmn_chk_dt")
        ilmn_chk_rslt_cd = list.get("ilmn_chk_rslt_cd")
        pbntTmng = list.get("pbntTmng")


    # 안전점검, 교육실시 현황
    req = urllib.request.urlopen(safety+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        estb_pt = list.get("estb_pt") # 설립유형
        fire_avd_yn = list.get("fire_avd_yn")
        fire_avd_dt = list.get("fire_avd_dt")
        gas_ck_yn = list.get("gas_ck_yn")
        gas_ck_dt= list.get("gas_ck_dt")
        fire_safe_yn = list.get("fire_safe_yn")
        fire_safe_dt = list.get("fire_safe_dt")
        elect_ck_yn = list.get("elect_ck_yn")
        elect_ck_dt = list.get("elect_ck_dt")
        plyg_ck_yn = list.get("plyg_ck_yn")
        plyg_ck_dt = list.get("plyg_ck_dt")
        plyg_ck_rs_cd = list.get("plyg_ck_rs_cd")
        cctv_ist_yn = list.get("cctv_ist_yn")
        cctv_ist_total = list.get("cctv_ist_total")
        cctv_ist_in = list.get("cctv_ist_in")
        cctv_ist_out = list.get("cctv_ist_out")
        pbntTmng = list.get("pbntTmng")
    

    # 공제회가입현황
    req = urllib.request.urlopen(deduc+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        estb_pt = list.get("estb_pt") # 설립유형
        school_ds_yn = list.get("school_ds_yn")
        school_ds_en = list.get("school_ds_en")
        educate_ds_yn = list.get("educate_ds_yn")
        ducate_ds_en = list.get("ducate_ds_en")
        pbntTmng = list.get("pbntTmng")

    # 보험별 가입 현황
    req = urllib.request.urlopen(insur+query) 
    res = req.readline()
    j = json.loads(res)
    jarray = j.get("kinderInfo")
    for list in jarray:
        kindername = list.get("kindername")
        officeedu = list.get("officeedu") # 교육청명
        subofficeedu = list.get("subofficeedu") # 교육지원청명
        kinderCode = list.get("kinderCode") # 유치원코드
        estb_pt = list.get("estb_pt") # 설립유형
        insurance_nm = list.get("insurance_nm")
        insurance_en = list.get("insurance_en")
        insurance_yn = list.get("insurance_yn")
        company1 = list.get("company1")
        company2 = list.get("company2")
        company3 = list.get("company3")
        pbntTmng = list.get("pbntTmng")


       
    
    # list 개수 만큼 db에 추가