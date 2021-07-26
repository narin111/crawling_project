from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# db.collection.count()

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbchildshcoolsite # local
collection = db.get_collection('eorini_test')


"""
유치원 개수 db 개수 비교하는 것은 어려울 것 같다.
-> 예외 경우가 많음 (정보입력이 안 된 유치원)
-> 어린이집은 폐원 필터링 안됨
=> selenium으로 count??
"""


def doc_count():
    cnt = db.eorini_test.count_documents( { 'kinderall' : 1 })
    return cnt 


def kinder_chk(kind):
    result = collection.find({ 'kinder_name' :  kind })
    print(kind)
    for kinderdoc in result:
        # print(i)
        for key, val in kinderdoc.items():
            print(key, ":", val)
            print("\n")
    print("\n\n")
    # myCursor = db.eorini_test.find({ 'kindername' :  kind })
    # print(myCursor.next())
    # print(myCursor.next())
    # return myCursor.next()


def test_doc_count():
    print(doc_count())
    assert doc_count() == 15189


def test_kinder_chk():
    kind_list = ["힐스테이트사임당어린이집", "스카이뷰어린이집", "다온어린이집", "에일린어린이집", "광성어린이집", "하얀돌어린이집", "풍림 어린이집"]
    for kind in kind_list:
        kinder_chk(kind)
        # print(dlist)
    assert True






