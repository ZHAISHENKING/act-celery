import random as rd


# 请求成功
def trueReturn(data):
    return {
        "code": 0,
        "data": data,
        "msg": "请求成功"
    }


# 内部错误
def falseReturn(msg):
    return {
        "code": 1,
        "data": '',
        "msg": msg
    }


# 无权限
def VaildReturn(data):
    return {
        "code": 4,
        "data": data,
        "msg": "无效验证"
    }


# 数据库操作错误
def MongoReturn():
    return {
        "code": 2,
        "msg": "数据库操作错误"
    }


# 错误判断
def catch_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        from flask import current_app
        from mongoengine.errors import (
            OperationError,
            FieldDoesNotExist,
            SaveConditionError,
            InvalidDocumentError,
            ValidationError,
            NotUniqueError,
            InvalidQueryError,
        )
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except AttributeError as e:
            return "字段错误"
        except (
            FieldDoesNotExist,
            SaveConditionError,
            InvalidQueryError,
            InvalidDocumentError,
            ValidationError,
            NotUniqueError,
            OperationError
        ) as e:
            current_app.logger.error(e)
            return MongoReturn()
        except TypeError as e:
            current_app.logger.error(e)
            return falseReturn("字段类型错误")
        except Exception as e:
            current_app.logger.error(e)
            return falseReturn("未知错误，请联系后台人员")

    return wrapper


def ms(d):
    import time
    # 给定时间元组,转换为秒
    return int(time.mktime(d.timetuple()))


# 生成4位手机验证码
def gen_verify_code(l=4):
    code = ""
    for i in range(l):
        code += str(rd.randint(0, 9))
    return code