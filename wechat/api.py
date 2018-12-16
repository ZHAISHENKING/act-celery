#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bson.objectid import ObjectId
from flask_restful import Resource
from util.utilb import *
from util.common import *
from mongoengine.queryset.visitor import Q
from homework.code import verify
from .models import *
from admin import limiter
from rsync_tasks import celery
from rsync_tasks.get_ip_city import get_ip


class OauthAct(Resource):
    """
    不同平台用户
    """

    @catch_exception
    def __init__(self):
        try:
            self.ip = request.headers["X-Forwarded-For"]
        except Exception:
            self.ip = request.remote_addr

    @catch_exception
    def post(self):
        """
        :param: code
        :param: name
        :param: phone
        :param: type
        :param: source
        :param: ip_city
        :return:
        """
        data = request.json
        if data["name"] and data["phone"]:

            if verify(data):
                a = OauthActivity.objects(Q(name=data["name"]) & Q(phone=data["phone"]))
                if a:
                    a.delete()

                try:
                    ip_city = get_ip.delay(self.ip)
                    ip_city = ip_city.get()
                except Exception:
                    ip_city = ""

                user = OauthActivity(
                    name=data["name"],
                    phone=data["phone"],
                    create_time=int(time.time()) * 1000,
                    type=data["type"],
                    source=data["source"],
                    ip_city=ip_city
                )

                user.save()

                if user.id:
                    return trueReturn(str(user["id"]))
                else:
                    return falseReturn("提交失败")

            else:
                return falseReturn("验证码错误")
        else:
            return falseReturn("请填写完整信息")

    @catch_exception
    def get(self):
        data = OauthActivity.objects.all()
        result = []
        if len(data):
            for i in data:
                obj = {
                    "id": str(i["id"]),
                    "name": i["name"],
                    "phone": i["phone"],
                    "create_time": i["create_time"],
                    "equipments": i["equipments"],
                    "sex": i["sex"],
                    "grade": i["grade"],
                    "Fname": i["fname"],
                    "type": i["type"],
                    "source": i["source"],
                    "ip_city": i["ip_city"]
                }
                result.append(obj)
        return trueReturn(result)


class OauthActInfo(Resource):
    @catch_exception
    def post(self):
        data = request.json
        info = OauthActivity.objects.filter(id=ObjectId(data["id"]))
        if info:
            info[0].update(
                fname=data["Fname"],
                equipments=data['equipments'],
                city=data['city'],
                sex=data['sex'],
                grade=data['grade']

            )
            return trueReturn("保存成功")
        else:
            return falseReturn("未查询到信息")


class GetActType(Resource):
    @catch_exception
    def post(self):
        data = request.json
        info = OauthActivity.objects.filter(type=data["type"])
        result = []
        if info:
            for i in info:
                obj = {
                    "id": str(i["id"]),
                    "name": i["name"],
                    "phone": i["phone"],
                    "create_time": i["create_time"],
                    "equipments": i["equipments"],
                    "sex": i["sex"],
                    "city": i["city"],
                    "grade": i["grade"],
                    "Fname": i["fname"],
                    "type": i["type"],
                    "source": i["source"]
                }
                result.append(obj)
        return trueReturn(result)
