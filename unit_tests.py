from unittest import TestCase
from pymongo import MongoClient

# db.collection.count()

client = MongoClient('localhost', 27017)
db = client.dbchildshcoolsite # local

class Mytests(TestCase):
    def test(self):
        self.assertEqual('d', 'd')

    def test_exceptions(self):
        1/0

    

# import unittest
# from mongoengine import connect, disconnect

# class Person(Document):
#     name = StringField()

# class TestPerson(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         connect('mongoenginetest', host='mongomock://localhost')

#     @classmethod
#     def tearDownClass(cls):
#        disconnect()

#     def test_thing(self):
#         pers = Person(name='John')
#         pers.save()

#         fresh_pers = Person.objects().first()
#         assert fresh_pers.name ==  'John'

