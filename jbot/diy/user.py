#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
import re
import sys
import time
import requests
import json
import datetime
from telethon import events, TelegramClient
import qrcode

from telethon.tl.types import ChannelForbidden
from .. import chat_id, jdbot, logger, api_id, api_hash, proxystart, \
    proxy, _ConfigDir, _JdDir, TOKEN, _ScriptsDir,QR_IMG_FILE,_ConfigDir


from ..bot.utils import cmd, V4, QL, _ConfigFile, myck
from ..diy.utils import getbean, my_chat_id, myzdjr_chatIds
from ..diy.utils import read, write, rwcon
import random
import traceback


from jbot.diy.config import bot_name


bot_id = int(TOKEN.split(":")[0])

if proxystart:
    client = TelegramClient("user", api_id, api_hash, proxy=proxy,
                            connection_retries=None)
else:
    client = TelegramClient("user", api_id, api_hash,
                            connection_retries=None)


# 监控高级user
@client.on(events.NewMessage(from_users=chat_id, pattern=r"^u$|^U$"))
async def user(event):
    try:
        msg = await event.respond(bot_name)
        await asyncio.sleep(1)
        await msg.delete()
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id,
                                 f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


_Auth = f'{_ConfigDir}/auth.json'


def mycron(lines):
    cronreg = re.compile(r'([0-9\-\*/,]{1,} ){4,5}([0-9\-\*/,]){1,}')
    return cronreg.search(lines).group()


@client.on(events.NewMessage(chats=[-1001235868507, 1716089227],from_users=[1049578757, chat_id]))
async def cmd_cron(event):
    try:
        if event.message.file:
            a = random.randint(1, 3000)
            filename = event.message.file.name
            path = f'{_ScriptsDir}/{filename}'
            if filename.endswith(".js") or filename.endswith(".py") or filename.endswith(".sh"):
                await client.download_media(event.message, file=path)
                with open(f'{_ScriptsDir}/{filename}', 'r',
                          encoding='utf-8') as f:
                    resp = f.read()
                cmdtext = f'task {_ScriptsDir}/{filename} now'
                try:
                    cron = mycron(resp)
                    await client.send_message(1716089227,f"{bot_name}识别的定时\n```{cron}```")
                except:
                    cron = '0 4 * * *'
                    await client.send_message(1716089227,f"{bot_name}无法识别定时，将使用默认定时\n```0 0 * * *```")
                crondata = {"name": f'{filename.split(".")[0]}{a}',
                            "command": f'task {path}',
                            "schedule": f'{cron}'}
                _Auth = f'{_ConfigDir}/auth.json'
                with open(_Auth, 'r', encoding='utf-8') as f:
                    auth = json.load(f)
                    token = auth['token']
                url = 'http://127.0.0.1:5600/api/crons'
                headers = {
                    'Authorization': f'Bearer {token}',
                }
                res = requests.post(url, data=crondata,
                                    headers=headers).json()
                await client.send_message(1716089227, f"{res}")
                if res['code'] !=200:
                    k_ram = random.randint(1, 7)
                    cron =f'12 {k_ram},6-23 * * *'
                    crondata = {"name": f'{filename.split(".")[0]}{random.randint(1, 3000)}',
                                "command": f'task {path}',
                                "schedule": f'{cron}'}
                    after_res = requests.post(url, data=crondata,
                                        headers=headers).json()
                    await client.send_message(1716089227, f"{after_res}")
                await cmd(cmdtext)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{filename}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(from_users=chat_id, pattern=r"^重启$"))
async def 重启机器人(event):
    try:
        await client.send_message(event.chat_id, f"正在重启机器人{bot_name}")
        cmdtext = r"if [ -d '/jd' ]; then cd /jd/jbot; pm2 start ecosystem.config.js; cd /jd; pm2 restart jbot; else ps -ef | grep 'python3 -m jbot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; nohup python3 -m jbot >/ql/log/bot/bot.log 2>&1 & fi"
        await cmd(cmdtext)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{e}")
        logger.error(f"错误--->{str(e)}")





@client.on(events.NewMessage(chats=1716089227,from_users=chat_id,
                             pattern=r'(export\s)?\w*=(".*"|\'.*\')'))
async def 增加export变量(event):
    try:
        messages = event.raw_text.split("\n")
        for message in messages:
            kv = message.replace("export ", "")
            kname = kv.split("=")[0]
            vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
            note = ''
            configs = read("str")
            configs += f'\nexport {kname}="{vname}"{note}'
            await asyncio.sleep(1.5)
            end = f"{bot_name}新增环境变量成功"
            write(configs)
            msg = await client.send_message(event.chat_id, end)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{e}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=-1001728533280,
                             pattern=r'export\s(jd_redrain_half_url|jd_redrain_activityId|jd_redrain_url).*=(".*"|\'.*\')'))
async def 京豆雨(event):
    try:
        text = event.message.text
        if "jd_redrain_half_url" in text:
            name = "半点京豆雨"
        elif "jd_redrain_activityId" in text:
            name = "整点京豆雨"
        elif "jd_redrain_url" in text:
            name = "整点京豆雨"
        else:
            return
        msg = await jdbot.send_message(chat_id,
                                       f'【监控】 监测到`{name}` 环境变量！')
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:
            if "export " not in message:
                continue
            kv = message.replace("export ", "")
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
            configs = rwcon("str")
            if kv in configs:
                continue
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            else:
                if V4:
                    end_line = 0
                    configs = rwcon("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            end_line = configs.index(config) - 1
                            break
                    configs.insert(end_line,
                                   f'export {key}="{value}"\n')
                else:
                    configs = rwcon("str")
                    configs += f'export {key}="{value}"\n'
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, f"【取消】 `{name}` 环境变量无需改动！")
            return
        try:
            if "jd_redrain_half_url" in event.message.text:
                await cmd('task /ql/data/scripts/jd_redrain_half.js now')
                msg = await jdbot.send_message(chat_id, r'`更换半点雨ID完毕')
                await asyncio.sleep(1)
                await jdbot.delete_messages(chat_id, msg)
            elif "jd_redrain_activityId" in event.message.text:
                await cmd('task /jd/scripts/jd_redrain.js now')
                msg = await jdbot.send_message(chat_id, r'`更换整点雨ID完毕')
                await asyncio.sleep(1)
                await jdbot.delete_messages(chat_id, msg)
            elif "jd_redrain_url" in event.message.text:
                await cmd('task /jd/scripts/jd_redrain.js now')
                msg = await jdbot.send_message(chat_id, r'`更换整点雨ID完毕')
                await asyncio.sleep(1)
                await jdbot.delete_messages(chat_id, msg)
            else:
                await jdbot.edit_message(msg, f"看到这行字,是有严重BUG!")
        except ImportError:
            pass
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id,
                                 f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=-1001320212725))
async def 关注店铺(event):
    try:
        message = event.message.text
        url = re.findall(
            re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S),
            event.message.text)
        if not url:
            return
        i = 0
        info = '关注店铺\n\n'
        for cookie in myck(_ConfigFile)[0]:
            i += 1
            if i <= 2:
                info += getbean(i, cookie, url[0])
                await asyncio.sleep(420)
            else:
                return
        await jdbot.send_message(chat_id, info)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=[-1001159808620, my_chat_id],
                             pattern=r".*京豆雨.*"))
async def red(event):
    """
    龙王庙京豆雨
    关注频道：https://t.me/longzhuzhu
    """
    try:
        file = "jredrain.sh"
        if not os.path.exists(f'{_JdDir}/{file}'):
            cmdtext = f'cd {_JdDir} && wget https://raw.githubusercontent.com/chiupam/JD_Diy/master/other/{file}'
            await cmd(cmdtext)
            if not os.path.exists(f'{_JdDir}/{file}'):
                await jdbot.send_message(chat_id,
                                         f"【龙王庙】\n\n监控到RRA，但是缺少{file}文件，无法执行定时")
                return
        message = event.message.text
        RRAs = re.findall(r'RRA.*', message)
        Times = re.findall(r'开始时间.*', message)
        for RRA in RRAs:
            i = RRAs.index(RRA)
            cmdtext = f"/cmd bash {_JdDir}/{file} {RRA}"
            Time_1 = Times[i].split(" ")[0].split("-")
            Time_2 = Times[i].split(" ")[1].split(":")
            Time_3 = time.localtime()
            year, mon, mday = Time_3[0], Time_3[1], Time_3[2]
            if int(Time_2[0]) >= 8:
                await client.send_message(bot_id, cmdtext,
                                          schedule=datetime.datetime(
                                              year, int(Time_1[1]),
                                              int(Time_1[2]),
                                              int(Time_2[0]) - 8,
                                              int(Time_2[1]), 0, 0))
            else:
                await client.send_message(bot_id, cmdtext,
                                          schedule=datetime.datetime(
                                              year, int(Time_1[1]),
                                              int(Time_1[2]) - 1,
                                              int(Time_2[0]) + 16,
                                              int(Time_2[1]), 0, 0))
            await jdbot.send_message(chat_id,
                                     f'监控到RRA：{RRA}\n预定时间：{Times[i].split("：")[1]}\n\n将在预定时间执行脚本，具体请查看当前机器人的定时任务')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id,
                                 f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=myzdjr_chatIds,
                             pattern=r"^export WxHbShare_AllUrl=\".*\"|^export gua_PopSign_venderId=\".*\"|^export gua_PopSign_shopId=\".*\"|^export gua_interact_activityUrl=\".*\"|^export jd_sign_activityUrl=\".*\"|^export CompleteInfo_AllUrl=\".*\"|^export pp_wuxian_activityUrl=\".*\"|^export jd_collectcard_activityUrl=\".*\"|^export jdjoyInvite_AllUrl=\".*\"|^export BirthGift_AllUrl=\".*\"|^export jd_smiek_package_activityUrl=\".*\"|^export pp_wxPointShopView_activityUrl=\".*\"|^export jd_smiek_luckDraw_activityUrl=\".*\"|^export jd_zdjr_.*=\".*\"|^export jd_smiek_addCart_activityUrl=\".*\"|^export jd_joinTeam3_activityId.*=\".*\"|^export OPEN_CARD_.*=\".*\"|^export FAV_.*=\".*\"|^export ISV_.*=\".*\"|^export RUSH_LZCLIENT.*=\".*\""))
async def 监控猪群变量(event):
    try:
        messages = event.message.text.split("\n")
        identity = ''
        msg = await jdbot.send_message(chat_id, "监控到新的活动变量，准备自动替换")
        end = ''
        for message in messages:
            if "export" not in message:
                continue
            if "jd_zdjr" in message:
                identity = "组队1"
            elif "joinTeam" in message:
                identity = "组队2"
            elif "FAV_" in message:
                identity = "收藏有礼"
            elif "ISV_" in message:
                identity = "关注有礼"
            elif "OPEN_CARD" in message:
                identity = "开卡"
            elif "RUSH_LZCLIENT" in message:
                identity = "转盘抽奖"
            elif "smiek_addCart_activityUrl" in message:
                identity = "加购入会"
            elif "luckDraw" in message:
                identity = "抽奖"
            elif "wxPointShopView" in message:
                identity = "积分兑换"
            elif "jd_smiek_package_activityUrl" in message:
                identity = "福袋"
            elif "BirthGift_AllUrl" in message:
                identity = "生日"
            elif "jdjoyInvite_AllUrl=" in message:
                identity = "邀请"
            elif "jd_collectcard_activityUrl" in message:
                identity = "集卡"
            elif "pp_wuxian_activityUrl" in message:
                identity = "pp"
            elif "CompleteInfo_AllUrl" in message:
                identity = "完善"
            elif "jd_sign_activityUrl" in message:
                identity = "sign"
            elif "gua_interact_activityUrl" in message:
                identity = "新活动"
            elif "gua_PopSign_shopId" in message:
                identity = "刮刮乐"
            elif "WxHbShare_AllUrl" in message:
                identity = "拆红包"
            kv = message.replace("export ", "").replace("*", "")
            kname = kv.split("=")[0]
            vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
            with open(f"{_ConfigDir}/config.sh", 'r',
                      encoding='utf-8') as f1:
                configs = f1.read()
            if kv in configs:
                continue
            if "jd_zdjr" in message and len(vname) != 32:
                msg = await jdbot.edit_message(msg,
                                               f"💀监控到{identity}变量，灵车竟想漂移入弯……")
                return
            if configs.find(kname) != -1:
                configs = configs.replace('`', '')
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv,
                                 configs)  # 替换值
                end = f"替换{identity}环境变量成功"
            else:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r',
                              encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find(
                                "↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 2,
                                   f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r',
                              encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"新增{identity}环境变量成功"
            with open(f"{_ConfigDir}/config.sh", 'w',
                      encoding='utf-8') as f3:
                f3.write(configs)
        if len(end) == 0:
            await jdbot.edit_message(msg,
                                     f"监控到{identity}变量，车坐过了取消执行!")
            return
        await jdbot.edit_message(msg, end)
        if "开卡" in identity:
            await cmd('task /ql/data/scripts/jd_open_card_by_shopid.js now')
        elif "组队2" in identity:
            await cmd("task /ql/data/scripts/gua_joinTeam3.js now")
        elif "收藏有礼" in identity:
            await cmd(
                'task /ql/data/scripts/jd_fav_shop_gift.js now')
        elif "关注有礼" in identity:
            await cmd(
                'task /ql/data/scripts/jspro_wxshop.js now')
        elif "组队1" in identity:
            await cmd(
                "task /ql/data/scripts/gua_zdjr.js now")
        elif "转盘抽奖" in identity:
            await cmd(
                "task /ql/data/scripts/rush_lzclient.js now")
        elif "加购入会" in identity:
            await cmd(
                "task /ql/data/scripts/gua_addCart.js now")
        elif "抽奖" in identity:
            await cmd(
                "task /ql/data/scripts/gua_luckDraw.js now")
        elif "积分" in identity:
            await cmd(
                "task /ql/data/scripts/pp_wxPointShopView.js now")
        elif "福袋" in identity:
            await cmd(
                "task /ql/data/scripts/jd_smiek_package.js now")
        elif "生日" in identity:
            await cmd(
                "task /ql/data/scripts/jd_BirthGifts.js now")
        elif "邀新" in identity:
            await cmd(
                "task /ql/data/scripts/gua_invite_join_shop.js now" )
        elif "集卡" in identity:
            await cmd(
                "task /ql/data/scripts/gua_collectcard.js now" )
        elif "pp" in identity:
            await cmd(
                "task /ql/data/scripts/pp_wuxian.js now" )
        elif "sign" in identity:
            await cmd(
                "task /ql/data/scripts/gua_shopsign2.js now" )
        elif "完善" in identity:
            await cmd(
                "task /ql/data/scripts/0jd_CompleteInfo.js now" )
        elif "新活动" in identity:
            await cmd(
                "task /ql/data/scripts/gua_interact.js now" )
        elif "刮刮乐" in identity:
            await cmd(
                "task /ql/data/scripts/gua_getPopSign.js now" )
        elif "看" in identity:
            await cmd(
                "task /ql/data/scripts/gua_getPopSign.js now" )
        elif "拆红包" in identity:
            await cmd(
                "task /ql/data/scripts/jd_WxHbShare.js now" )
        else:
            await jdbot.edit_message(msg, f"看到这行字,是有严重BUG!")
    except Exception as e:
        await jdbot.send_message(chat_id,
                                 'something wrong,I\'m sorry\n' + str(
                                     e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@client.on(events.NewMessage(chats=myzdjr_chatIds,
                             pattern=r'(export\s)?MyShopToken\d*=(".*"|\'.*\')'))
async def myshoptoken(event):
    try:
        messages = event.message.text.split("\n")
        exports = re.findall(r'export MyShopToken(\d+)="(.*)"',
                             rwcon("str"))
        change, line, number = "", 0, 1
        if not exports:
            msg = await jdbot.send_message(chat_id,
                                           '监控到店铺签到环境变量，直接添加！')
            configs = rwcon("str")
            for message in messages:
                value = re.findall(r'"([^"]*)"', message)[0]
                if V4:
                    configs = rwcon("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            line = configs.index(config)
                            break
                    change += f'export MyShopToken1="{value}"\n'
                    configs.insert(line - 2,
                                   f'export MyShopToken1="{value}"\n')
                elif QL:
                    change += f'export MyShopToken1="{value}"\n'
                    configs += f'export MyShopToken1="{value}"\n'
                rwcon(configs)
            await jdbot.edit_message(msg,
                                     f"【店铺签到领京豆】\n\n此次添加的变量\n{change}")
            return
        msg = await jdbot.send_message(chat_id, '监控到店铺签到环境变量，继续添加！')
        for message in messages:
            value = re.findall(r'"([^"]*)"', message)[0]
            configs = rwcon("str")
            if value in configs:
                continue
            configs = rwcon("list")
            for config in configs:
                if "export MyShopToken" in config:
                    number = int(
                        re.findall(r'\d+', config.split("=")[0])[
                            0]) + 1
                    line = configs.index(config) + 1
            change += f'export MyShopToken{number}="{value}"\n'
            configs.insert(line,
                           f'export MyShopToken{number}="{value}"\n')
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, "目前配置中的环境变量无需改动")
            return
        await jdbot.edit_message(msg,
                                 f"【店铺签到领京豆】\n\n此次添加的变量\n{change}")
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id,
                                 f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")




def creat_qr(text):
    '''实例化QRCode生成qr对象'''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.clear()
    # 传入数据
    qr.add_data(text)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    # 保存二维码
    img.save(QR_IMG_FILE)

@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'^/userlogin$'))
async def user_login(event):
    try:
        await client.connect()
        qr_login = await client.qr_login()
        creat_qr(qr_login.url)
        await jdbot.send_message(chat_id,'请使用TG扫描二维码以开启USER',file=QR_IMG_FILE)
        await qr_login.wait(timeout=100)
        await jdbot.send_message(chat_id,'恭喜您已登录成功,请修改 /set 将开启user 改为True 并重启机器人 /reboot')
    except Exception as e:
        await jdbot.send_message(chat_id,'登录失败\n'+str(e))

@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'^/rmuser$'))
async def user_login(event):
    try:
        await jdbot.send_message(chat_id,'即将删除user.session')
        os.remove(f'{_ConfigDir}/user.session')
        await jdbot.send_message(chat_id,'已经删除user.session\n请重新登录')
    except Exception as e:
        await jdbot.send_message(chat_id,'删除失败\n'+str(e))
