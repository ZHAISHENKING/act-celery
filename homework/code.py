from flask import request, session, jsonify, current_app
from flask_restful import Resource
from util.common import *
from util.sms import SMS
from admin import r

s = SMS()


class PhoneCode(Resource):
    def post(self):
        d = request.json
        nation = 86
        phone = d["phone"]
        time_out = d["timeOut"]
        res = s.send(nation, phone, time_out)
        r.set("slag", "0")
        return jsonify(s.handle(res))


def verify(data):
    d = data
    nation = 86
    phone = d["phone"]
    code = d["code"]
    a = s.verify(nation, phone, code)
    if a["code"] == 0:
        return True
    else:
        return False


class PhoneCodeVerify(Resource):
    """手机验证码验证"""
    @catch_exception
    def post(self):
        d = request.get_json()
        nation = 86
        phone = d["phone"]
        code = d["code"]
        a = s.verify(nation, phone, code)
        if a["code"] == 0:
            r.set("slag", "1")
            return trueReturn("ok")
        else:
            return falseReturn("验证失败")