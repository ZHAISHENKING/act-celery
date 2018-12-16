from admin import db
from datetime import datetime


class Student(db.Document):
    """
    报名信息
    """
    sexChoice = ((0, '女'),
                   (1, '男'))
    gradeChoice = (1,2,3,4,5,6)

    name = db.StringField()
    fname = db.StringField()
    grade = db.IntField(choice=gradeChoice)
    phone = db.StringField()
    equipments = db.ListField(db.StringField(max_length=50))
    sex = db.IntField(choice=sexChoice)
    city = db.StringField()
    create_time = db.IntField()
    source = db.StringField()


class File(db.Document):
    """
    文件
    """
    filename = db.StringField()
    size = db.IntField()
    content = db.BinaryField()
    md5 = db.StringField()
    time = db.DateTimeField()
    mime = db.StringField()


class Day(db.Document):
    """
    优秀作品
    """
    name = db.StringField()
    homeWork = db.StringField()
    imgfile = db.StringField()
    text = db.StringField()
    comments = db.StringField()
    kadaUrl = db.StringField()
    title = db.StringField()
    videofile = db.StringField()
    create_time = db.IntField()


class Consultation(db.Document):
    """
    官网咨询
    """
    name = db.StringField(required=True, max_length=30)
    phone = db.StringField(length=20)
    create_date = db.DateTimeField(default=datetime.now)


class ClassInfo(db.Document):
    """
    学生年级信息表
    """
    name = db.StringField(required=True, max_length=30)
    phone = db.StringField(required=True, max_length=20)
    class_level = db.StringField()
    create_date = db.DateTimeField(default=datetime.now)


class Activity(db.Document):
    """
    9.20 作业帮活动
    """
    sexChoice = ((0, '女'),
                 (1, '男'))
    gradeChoice = (1, 2, 3, 4, 5, 6)

    name = db.StringField()
    fname = db.StringField()
    grade = db.IntField(choice=gradeChoice)
    phone = db.StringField()
    equipments = db.ListField(db.StringField(max_length=50))
    sex = db.IntField(choice=sexChoice)
    city = db.StringField()
    create_time = db.IntField()
    source = db.StringField()


class Operation(db.Document):
    """
    获取用户页面停留等行为
    """
    user_name = db.StringField()
    user_ip = db.StringField()
    country = db.StringField()
    stay_time = db.IntField(default=0)
    router = db.StringField()
    create_time = db.IntField()

