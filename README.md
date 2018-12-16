# ultrabear-activity

活动页面	

| 功能         | Method | URL                     | Field                                        |
| ------------ | ------ | ----------------------- | -------------------------------------------- |
| 文件展示     | POST   | /docs/f/<id>/           | id                                           |
| 获取作品信息 | GET    | /docs/student_all/<id>/ | id                                           |
| 添加学生报名 | POST   | /docs/student/          | name  phone                                  |
| 查看报名学生 | GET    | /docs/student/          |                                              |
| 补充完整信息 | POST   | /docs/student_info/     | id， fname ，equipments， city， sex， grade |