from homework.api import *
from flask import Blueprint
from flask_restful import Api
from admin import LogoutView, LoginView, Index
from homework.code import PhoneCode
from wechat.api import *

# 注册蓝图,路由前缀为/docs
uploadApi = Blueprint('api', __name__, url_prefix='/docs')

docs = Api(uploadApi)

# docs.add_resource(Index,'/', endpoint='home')                                         # 测试表单
docs.add_resource(ServerFile, '/f/<id>/', endpoint='serverfile')                        # 文件展示
docs.add_resource(UploadAPI, '/upload/', endpoint='upload')                             # 上传接口
docs.add_resource(HomeworkInfoAPI, '/student_all/<id>/', endpoint='homeinfo')           # 获取作品信息
docs.add_resource(StudentAppAPI,'/student/', endpoint='student')                        # 添加学生报名信息
docs.add_resource(StudentInfoAPI, '/student_info/', endpoint='studentinfo')             # 补全学生信息
docs.add_resource(Info, '/info/')                                                       # 官网咨询学生信息
docs.add_resource(StudentWebAPI, '/web/student/')                                       # 官网咨询学生信息补全
docs.add_resource(Index, '/', endpoint="index")                                         # 后台首页
docs.add_resource(LoginView, '/login/', endpoint="login")                               # 后台登录页
docs.add_resource(LogoutView, '/logout/', endpoint="logout")                            # 退出登录
docs.add_resource(Act, '/activity/', endpoint='activity')                               # 作业帮保存用户信息
docs.add_resource(PhoneCode, '/sms_code/')                                              # 手机验证码
docs.add_resource(ActInfo, '/act_info/')                                                # 作业帮补充用户信息
docs.add_resource(OauthAct, '/oauth_activity/')                                         # 微信多平台添加用户
docs.add_resource(OauthActInfo, '/oauth_info/')                                         # 微信多平台用户补全信息
docs.add_resource(GetActType, '/get_act/')                                              # 返回某个平台用户
# docs.add_resource(AddStayUser, '/add_operation/')                                       # 用户访问记录
# docs.add_resource(StayUser, '/operation/')                                              # 更新访客记录
docs.add_resource(Paging, '/paging/')                                                   # 访客记录分页
