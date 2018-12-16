#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import bson.binary
import bson.objectid
import bson.errors
from bson.objectid import ObjectId
from flask import redirect, make_response, current_app, Response, send_from_directory
from flask_restful import Resource
from util.utilb import *
from util.common import *
from .models import Student, Day, File, Consultation, ClassInfo, Activity, Operation
from mongoengine.queryset.visitor import Q
from .code import verify
from admin import limiter


class UploadAPI(Resource):

    def get(self):
        return redirect('https://course.ultrabear.com.cn/shareday')

    def post(self):
        data = request.values
        image = request.files['imgfile']
        imageurl = save_file(image)
        # 视频可为空
        if 'videofile' in request.files:
            video = request.files['videofile']
            videourl = save_file(video)
            videofile = '/f/' + str(videourl)
        else:
            videofile = ''

        student10 = {"name": data['name'],
                     "homeWork": data['homeWork'],
                     "comments": data['comments'],
                     "videofile": videofile,
                     "imgfile": '/f/' + str(imageurl),
                     "kadaUrl": data['kadaUrl'],
                     "title": data['title'],
                     "text": data['text'],
                     "create_time": int(time.time())*1000
                     }

        student = Day(**student10).save()
        student_id = student['id']
        student_ids = str(ObjectId(student_id))
        data = {
            "code": 200,
            "msg": "上传成功",
            "data": student_ids
        }
        return responseto(data=data)


class ServerFile(Resource):
    """
    查看作品视频
    """
    def get(self, id):
        md = File.objects(md5=id.split('.')[0]).first()
        if md is None:
            raise bson.errors.InvalidId()
        mime = current_app.config["ALLOWED_EXTENSIONS"][md['mime']]
        if md['content']:
            f = ""
            resp = Response(md['content'], mimetype=mime)
        else:
            return send_from_directory("/data/static/uploads", id)

        resp.headers['Last-Modified'] = md['time'].ctime()
        ctype = mime
        if request.headers.get("Range"):
            range_value = request.headers["Range"]
            HTTP_RANGE_HEADER = re.compile(r'bytes=([0-9]+)\-(([0-9]+)?)')
            m = re.match(HTTP_RANGE_HEADER, range_value)
            if m:
                start_str = m.group(1)
                start = int(start_str)
                end_str = m.group(2)
                end = -1
                if len(end_str) > 0:
                    end = int(end_str)
                resp.status_code = 206
                resp.headers["Content-Type"] = "video/mp4"
                if end == -1:
                    resp.headers["Content-Length"] = str(md['size'] - start)
                else:
                    resp.headers["Content-Length"] = str(end - start + 1)
                resp.headers["Accept-Ranges"] = "bytes"
                if end < 0:
                    content_range_header_value = "bytes %d-%d/%d" % (start, md['size'] - 1, md['size'])
                else:
                    content_range_header_value = "bytes %d-%d/%d" % (start, end, md['size'])
                resp.headers["Content-Range"] = content_range_header_value
                resp.headers["Connection"] = "close"
        resp.status_code = 200
        return resp


class HomeworkInfoAPI(Resource):
    """
    查看作品信息
    """
    def get(self, id):
        try:
            obj = Day.objects(id=ObjectId(id)).first()
            data = {
                "code": 200,
                "msg": "请求成功",
                "data": {
                    'name': obj["name"],
                    "homeWork": obj["homeWork"],
                    "comments": obj["comments"],
                    "videofile": obj["videofile"],
                    "imgfile": obj["imgfile"],
                    "title": obj["title"],
                    "text": obj["text"],
                    "kadaUrl": obj["kadaUrl"],
                    "create_time": obj["create_time"]
                }
            }
            return responseto(data=data)
        except Exception as e:
            return {'msg': '信息不存在'}, 404


class StudentAppAPI(Resource):
    """
    存储微信活动页学生报名信息
    """
    def get(self):
        try:
            result = []
            obj = Student.objects.all()
            for i in obj:
                result.append({
                    "name": i['name'],
                    "phone": i["phone"],
                    "Fname": i['fname'],
                    "equipments": i["equipments"],
                    "grade": i["grade"],
                    "sex": i["sex"],
                    "city": i["city"],
                    "create_time": i["create_time"],
                    "source": i["source"]
                })
            data = {
                "code": 200,
                "msg": "请求成功",
                "data": result
            }
            return responseto(data=data)
        except Exception as e:
            current_app.logger.error(e)
            return {'code':400, 'msg': '信息不存在'}

    def post(self):
        data = request.get_json()
        infoIO = {
            "name": data['name'],
            "phone": data["phone"],
            "fname": '',
            "equipments": [''],
            "grade": 0,
            "sex": 2,
            "city": '',
            "create_time": int(time.time())*1000,
            "source": data["source"]

        }
        try:
            user = Student(**infoIO)
            user.save()
            data = {
                "code": 200,
                "msg": "上传成功",
                "data": str(user['id'])
            }
            return responseto(data=data)
        except Exception as e:
            current_app.logger.error(e)
            return {"msg": "保存失败",'code':400}


class StudentInfoAPI(Resource):
    """报名完整信息"""
    def post(self):
        try:
            data = request.get_json()
            user = Student.objects(id=ObjectId(data['id'])).first()
            user.update(
                fname=data["Fname"],
                equipments=data['equipments'],
                city=data['city'],
                sex=data['sex'],
                grade=data['grade'],
                create_time=int(time.time())*1000
            )
            return {'msg': '保存成功', 'code':200}
        except Exception as e:
            current_app.logger.error(e)
            return {'msg':'保存失败', 'code':400}


class Info(Resource):
    """
    存取官网咨询人员信息
    """
    @catch_exception
    def post(self):
        data = request.get_json()
        if data["name"] and data["phone"]:
            a = Consultation.objects(Q(name=data["name"]) & Q(phone=data["phone"]))
            if a:

                user = Consultation(
                    name=data["name"],
                    phone=data["phone"]
                )
                user.save()
                a.delete()
                return trueReturn("预约成功～")
            else:
                user = Consultation(
                    name=data["name"],
                    phone=data["phone"]
                )
                user.save()
                return trueReturn("OK")
        else:
            return falseReturn("请填写完整信息")

    @catch_exception
    def get(self):
        data = Consultation.objects.all()
        result = []
        if len(data):
            for i in data:
               obj = {
                   "name": i["name"],
                   "phone": i["phone"],
                   "create_date": ms(i["create_date"])*1000
               }
               result.append(obj)
        return trueReturn(result)


class StudentWebAPI(Resource):
    """
    官网学生预约课信息
    """
    @catch_exception
    def get(self):
        class_info = ClassInfo.objects.all()
        result = []
        if len(class_info):
            for i in class_info:
               obj = {
                   "name": i["name"],
                   "phone": i["phone"],
                   "class_level": i["class_level"],
                   "create_date": ms(i["create_date"])*1000
               }
               result.append(obj)
        return trueReturn(result)

    @catch_exception
    def post(self):
        data = request.get_json()
        if data["name"] and data["phone"]:
            a = ClassInfo.objects(Q(name=data["name"]) & Q(phone=data["phone"]))
            if a:
                return falseReturn("信息已存在，请勿重复提交")
            else:
                info = ClassInfo(
                    name=data["name"],
                    phone=data["phone"],
                    class_level=data["class_level"]
                )
                info.save()
                return trueReturn("OK")
        else:
            return falseReturn("请填写完整信息")


class Act(Resource):
    """
    9.20作业帮活动
    领取试听课礼包
    """
    @catch_exception
    def post(self):
        """
        :param: code
        :param: name
        :param: phone
        :param: source
        :return:
        """
        data = request.json
        if data["name"] and data["phone"]:
            if verify(data):
                a = Activity.objects(Q(name=data["name"]) & Q(phone=data["phone"]))
                if a:
                    return falseReturn("信息已存在，请勿重复提交")
                else:
                    user = Activity(
                        name=data["name"],
                        phone=data["phone"],
                        create_time=int(time.time()) * 1000,
                        source=data["source"]
                    )
                    user.save()
                    return trueReturn(str(user["id"]))
            else:
                return falseReturn("验证码错误")
        else:
            return falseReturn("请填写完整信息")

    @catch_exception
    def get(self):
        data = Activity.objects.all()
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
                    "city": i["city"],
                    "grade": i["grade"],
                    "Fname": i["fname"],
                    "source": i["source"]
                }
                result.append(obj)
        return trueReturn(result)


class ActInfo(Resource):
    @catch_exception
    def post(self):
        data = request.json
        info = Activity.objects.filter(id=ObjectId(data["id"]))
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


class AddStayUser(Resource):
    """新增访客记录"""
    @catch_exception
    def __init__(self):
        # self.ip = request.remote_addr
        self.ip = request.headers["X-Forwarded-For"]
        resp = requests.get(
            url="http://ip.taobao.com/service/getIpInfo.php?ip=%s" % self.ip,
        )
        if resp:
            self.resp = resp.json()
        else:
            self.resp = ''

    def get(self):
        city = self.resp
        obj = {
            "user_ip": self.ip,
            "country": city["data"]["region"] + city["data"]["city"] if city else "",
            "create_time": int(time.time())*1000
        }
        op = Operation(**obj)
        op.save()
        return trueReturn(str(op.id))


class StayUser(Resource):
    """更新访客记录"""
    @catch_exception
    def __init__(self):
        # self.ip = request.remote_addr
        self.ip = request.headers["X-Forwarded-For"]

    @catch_exception
    def get(self):
        all = Operation.objects.all()
        result = []
        if all:
            for i in all:
                obj = {
                    "id": str(i.id),
                    "user_ip": i.user_ip,
                    "timeout_name": i.user_name,
                    "country": i.country,
                    "timeout": i.stay_time,
                    "router": i.router,
                    "create_time": i.create_time
                }
                result.append(obj)
        return trueReturn(result)

    @catch_exception
    def post(self):
        data = request.json
        op = Operation.objects.filter(id=ObjectId(data["id"]))
        if op:
            obj = {
                "user_ip": self.ip,
                "stay_time": int(data["timeout"]),
                "user_name": data["timeout_name"],
                "router": data["router"],
            }
            
            if not op[0]["country"]:
                resp = requests.get(
                    url="http://ip.taobao.com/service/getIpInfo.php?ip=%s" % self.ip,
                )
                if resp:
                    self.resp = resp.json()
                else:
                    self.resp = ""

                city = self.resp
                obj["country"] = city["data"]["region"] + city["data"]["city"] if city else ""
            op[0].update(**obj)
            
            return trueReturn(str(op["id"]))
        else:
            return falseReturn("记录不存在")


class Paging(Resource):
    """分页"""
    @catch_exception
    def post(self):
        import math
        data = request.json
        # 每页多少条
        num = int(data["num"])
        # 第几页
        page = int(data["page"])
        # 总数据条数
        total = Operation.objects.all().count()
        # 共多少页
        pages = math.ceil(total / num)
        # 起始条数
        start = num*(page-1)
        end = num*page
        # 最终数据
        all = Operation.objects[start:end]
        list = []
        if all:
            for i in all:
                obj = {
                    "id": str(i.id),
                    "user_ip": i.user_ip,
                    "timeout_name": i.user_name,
                    "country": i.country,
                    "timeout": i.stay_time,
                    "router": i.router,
                    "create_time": i.create_time
                }
                list.append(obj)
        # 返回结果
        result = {
            "data": list,
            "total": total,
            "pages": pages
        }
        return trueReturn(result)