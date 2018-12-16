# 项目说明

> 此项目缺少执行所需PRD文件无法运行,主要记录celery在flask工厂模式项目中运行所踩的坑

所需模块

```bash
Celery
Flask-Celery-Helper
Flask-And-Redis
```

### 基本配置

配置celery主要的几个文件是 `rsync_task`目录中的两个文件`__init__.py`作为实例化入口, `app.py`作为init_app入口，`config.py`填写redis参数和celery运行所需的`borker`,`backend`参数,`get_ip_city`写需要异步执行的函数`get_ip`, `wechat`目录下的`api.py`中调用`get_ip`方法

celery运行命令`celery worker -A manage.celery --loglevel=info`
