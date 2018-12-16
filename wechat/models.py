from admin import db

sexChoice = ((0, '女'),
                 (1, '男'))
gradeChoice = (1, 2, 3, 4, 5, 6)


class OauthActivity(db.Document):
    """
    记录不同平台不同来源的活动
    """
    name = db.StringField()
    fname = db.StringField()
    grade = db.IntField(choice=gradeChoice)
    phone = db.StringField()
    equipments = db.ListField(db.StringField(max_length=50))
    sex = db.IntField(choice=sexChoice)
    city = db.StringField()
    create_time = db.IntField()
    source = db.StringField()
    type = db.StringField()
    ip_city = db.StringField()
