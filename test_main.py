import json

import unittest

from abc import ABC
from base64 import b64encode

from flask import jsonify
from flask_login import test_client
from flask_testing import TestCase

from app import *



med_id = 23
user_id_to_delete=42
user_id = 20



class TestStringMethods(TestCase, ABC):

    def setUp(self):

        pass



    def create_app(self):

        return app



    def test_00_createUser(self):

        response = self.client.post('/user', data=json.dumps({"username":"test144we",
                                                                    "first_name":"test",
                                                                    "email":"test",
                                                                    "password":"test",
                                                                    "phone":"phone",
                                                                    "roles":"admin"}),content_type="application/json")



        self.assertEqual(response.json, None)



    def test_01_login(self):



        response = self.client.post('/user/login', data=json.dumps({

            "username": "test","password": "test"}), content_type="application/json")





    def test_02_get_user(self):

        global  user_id

        credentials = b64encode(b"test:test").decode('utf-8')
        response= self.client.get("/user/test?", headers={"Authorization": f"Basic {credentials}"})
        self.assertNotEqual(response.json, None)



    def test_03_add_med(self):

        global user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.post('/medicine', data=json.dumps({

                                        "name": "test144",
                                        "price": 123,
                                        "number": 23,
                                        "photo_url": "test",
                                        "description": "desc"}),

                                    headers={"Authorization": f"Basic {credentials}","Content-type": "application/json"})

        self.assertEqual(response.json, None)



    def test_04_update_medicine(self):

        global  med_id, user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.put('/medicine' , data=json.dumps({

            "id": 2,
            "data": {
                "price": 113,
                "number": 2

            }

        }), headers={"Authorization": f"Basic {credentials}","Content-type": "application/json"})

        self.assertEqual(response.json, None)

    def test_24_update_medicine(self):

        global  med_id, user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.put('/medicine' , data=json.dumps({

            "id": 100000,
            "data": {
                "price": 113,
                "number": 2

            }

        }), headers={"Authorization": f"Basic {credentials}","Content-type": "application/json"})

        self.assert404(response)

    def test_05_get_med(self):

        global med_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.get('/medicine/{0}'.format(4))
        print(response)
        self.assertNotEqual(response.json,None)

    def test_06_get_med(self):

        global med_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.get('/medicine/{0}'.format(4000))
        print(response)
        self.assert404(response)






    def test_07_delete_medicine(self):

        global  med_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.delete('/medicine/{0}?'.format(med_id),  headers={"Authorization": f"Basic {credentials}"})

        self.assertEqual(response.json, None)



    def test_08_add_order(self):
        global user_id, med_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.post('/store/order', data=json.dumps({

                                                "user_id":6,
                                                "medicine_id":2}),

                                    headers={"Authorization": f"Basic {credentials}","Content-type": "application/json"})

        self.assertEqual(response.json, None)



    def test_09_delete_user(self):

        global  user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.delete('/user/{0}?'.format(user_id_to_delete),

                                      headers={"Authorization": f"Basic {credentials}"})

        self.assert200(response)
    def test_10_a(self):
        global user_id

        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.get("/user/test?", headers={"Authorization": f"Basic {credentials}"})
        self.assertNotEqual(response.json, None)

    def test_11_createUser(self):
        User('nemo','sadsa','sdasd','asdasdas','asdasd').__repr__()


    def test_12_createOrder(self):
        Order('1','2').__repr__()
    def test_13_createMed(self):
        Med('asd',1,2,'wqewwd').__repr__()

    def test_14_chekpassw(self):
        views.verify_password('test','test')
    def test_15_wrongdata(self):
        response = self.client.post('/user', data=json.dumps({"username": "test294d779we",
                                                              "first_name": "test",

                                                              "password": "test",
                                                              "phone": "phone",
                                                              "roles": "admin"}), content_type="application/json")
        self.assert400(response)
    def test_16_already_registered_user(self):
        response = self.client.post('/user', data=json.dumps({"username": "test294779we",
                                                              "first_name": "test",
                                                              "email": "test",
                                                              "password": "test",
                                                              "phone": "phone",
                                                              "roles": "admin"}), content_type="application/json")

        self.assertEqual(response.json, None)
    def test_17_wrong_datatype(self):
        global user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.post('/medicine', data=json.dumps({

            "name": "test1288",
            "price": 123,
            "number": "23",
            "photo_url": "test",
            "description": "desc"}),

                                    headers={"Authorization": f"Basic {credentials}",
                                             "Content-type": "application/json"})

        self.assert400(response)
    def test_18_logout(self):
        response = self.client.get('/logout')
        self.assert401(response)

    def test_19_get_not_med(self):
        pass
    def test_20_delete_not_user(self):

        global  user_id
        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.delete('/user/{0}?'.format("huhih"),

                                      headers={"Authorization": f"Basic {credentials}"})

        self.assert400(response)
    def test_21_get_not_user(self):
        global user_id

        credentials = b64encode(b"test:test").decode('utf-8')
        response = self.client.get("/user/testdsfdsfdsfdsfdsf?", headers={"Authorization": f"Basic {credentials}"})
        self.assert404(response)
    if __name__ == 'main':

        unittest.main()

