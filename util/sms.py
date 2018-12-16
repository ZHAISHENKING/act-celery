from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from .common import *
from production import *
try:
    from local_settings import *
except Exception:
    pass
from util.common import falseReturn


class SMS(object):
    """发送短信接口"""
    def __init__(self, appid=appid, appkey=appkey):
        self.ssender = SmsSingleSender(appid, appkey)
        self.buffer = {}

    def send(self, nation, phone, time_out):

        code = gen_verify_code(4)
        params = [code, str(time_out)]
        self.buffer[phone] = code
        template_id = 97249
        try:
            res = self.ssender.send_with_param(
                nationcode=nation,
                phone_number=phone,
                template_id=template_id,
                params=params
           )
        except HTTPError as e:
            print(": ")
            print(e)
            return falseReturn("网络错误")
        except Exception as e:
            print("Exception: ")
            print(e)
        else:
            print("send sms to {0}-{1}, code is {2}".format(nation, phone, code))
            return res

    def verify(self, nation, phone, code):
        """
        :param nation: int: 86
        :param phone: str: "12345678901"
        :param code: str: "1234"
        :return: bool: True if verified, else False
        """

        # nation, phone = split_phone(full_phone)
        if not phone in self.buffer:
            print("Phone number not registered")
            return falseReturn("手机号不匹配")
        else:
            vrf = self.buffer[phone] == code
        if vrf:
            print("verify success, {0}-{1}: {2}".format(nation, phone, code))
            del self.buffer[phone]
            return trueReturn("验证成功")
        else:
            print("verify fail, {0}-{1} should be {2} but recv {3}".format(nation, phone, self.buffer[phone], code))
            return falseReturn("手机验证失败")

    def handle(self, res):
        result = res["result"]
        errmsg = res["errmsg"]
        err_choice = dict([
            (0, "发送成功"),
            (1013, "下发短信/语音命中了频率限制策略"),
            (1016, "手机号格式错误"),
            (1022, "业务短信日下发条数超过设定的上限"),
            (1023, "单个手机号 30 秒内下发短信条数超过设定的上限"),
            (1024, "单个手机号 1 小时内下发短信条数超过设定的上限"),
            (1025, "单个手机号日下发短信条数超过设定的上限")
        ])
        if result == 0:
            return trueReturn("发送成功")
        elif result in err_choice:
            return falseReturn(err_choice[result])
        else:
            return falseReturn("发送失败")
