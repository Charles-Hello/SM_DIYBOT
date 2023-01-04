# -*- coding: utf-8 -*-
"""
@Time ： 2022/3/30 14:13
@Auth ： maomao
@File ：config.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import requests
import json


dormitory = '12361142051@chatroom'
tnanko = 'wxid_xq2w7jl6cbi811'
jd_xianbao = '5748551094@chatroom'
jd_miaomiaomiao = "19244435890@chatroom"
group_id = '24446492186@chatroom'
user_id = 'wxid_p8geau233z3412'
taobao_fuli = '17573440617@chatroom'
taobao_xianbao = '5739151628@chatroom'


bot_name = '管理员'


#第一个bot_id作为管理员！其他都是工具user
ql_bot =[1768732953,1777317008,1725882570,1636528445,5100477160]

#存放日记的bot
ql_log_bot=1751599830



bot_url = "http://192.168.1.50:8090"
bot_headers = {
    'Name': 'iHttp',
    'Ver': "1.1.4.1",
    'Udid': '0b4891edc500803721b76cf782200fd3',
}
def send_text_msg(robot_wxid, to_wxid, msg):
    """
    发送普通文本消息
    :param robot_wxid:机器人ID
    :param to_wxid:消息接收ID 人/群
    :param msg:文本消息
    :return:发送消息
    """
    data = dict()
    data["event"] = "SendTextMsg"
    data["robot_wxid"] = robot_wxid
    data["to_wxid"] = to_wxid
    data["msg"] = msg
    result = json.dumps(data)

    requests.post(url=bot_url, data=result, headers=bot_headers)

