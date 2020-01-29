from flask import Flask, request,jsonify,Response,make_response
from flask_apscheduler import APScheduler
import requests
import time


class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        # {  # 第一个任务
        #     'id': 'job1',
        #     'func': '__main__:job_1',
        #     'args': (1, 2),
        #     'trigger': 'cron', # cron表示定时任务
        #     'hour': 19,
        #     'minute': 27
        # },
        {  # 第二个任务，每隔5S执行一次
            'id': 'job2',
            'func': '__main__:method_test',  # 方法名
            'args': (1, 2),  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 5000,
        }
    ]

provinceName = "湖北省"
cityName = "西安市"


class Lib:
    def timestamp(self,timestamp):
        # 转换成localtime
        time_local = time.localtime(int(timestamp)/1000)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local).split(" ")[0]
        return dt

lib = Lib()


class Disease:
    def __init__(self):
        self.base_uri = "http://lab.isaaclin.cn"
        self.history_msg = {}
    def city(self):
        pass
    def province(self):
        uri = self.base_uri + "/nCoV/api/area?province="+provinceName+"&latest=0"
        r = requests.get(uri)
        dicts = {}
        for line in r.json()["results"]:
            print(lib.timestamp(timestamp=line["updateTime"]))
            dicts[lib.timestamp(timestamp=line["updateTime"])] = line["confirmedCount"]

        return dicts







disease = Disease()


def method_test(a, b):
    print(a + b)


app = Flask(__name__,static_url_path="")
app.config.from_object(Config())  # 为实例化的flask引入配置

@app.route('/')
def index():
    return app.send_static_file('index.html')

##
@app.route("/api", methods=["POST", "GET"])
def check():

    return make_response(jsonify(
        {
            "area":provinceName,
            "count":disease.province()

        }
    ))







if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)