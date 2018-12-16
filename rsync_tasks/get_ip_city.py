from rsync_tasks import celery
import requests


@celery.task()
def get_ip(ip):
    resp = requests.get(
        url="http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    )
    if resp:
        city = resp.json()
    else:
        city = ""
    ip_city = city["data"]["region"] + city["data"]["city"] if city else ""

    return ip_city


@celery.task()
def add(x, y):
    return x + y