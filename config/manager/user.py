#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import datetime
import os
import re
import sys
import requests
from telethon import events, TelegramClient,functions
from .. import chat_id, jdbot, logger, api_id, api_hash, proxystart, \
    proxy, _ConfigDir, _JdDir, TOKEN, _JdbotDir, _ScriptsDir
from ..bot.utils import cmd, V4, QL, _ConfigFile, myck, backfile
from ..diy.utils import getbean, my_chat_id, myzdjr_chatIds, \
    shoptokenIds
from ..diy.utils import read, write, rwcon
import random
import json
from datetime import datetime
import time
from  ..diy.configpro import send_text_msg, bot_name, bot_url, bot_headers, \
    ql_bot, ql_log_bot, user_id, tnanko
import traceback
from telethon.tl.types import ChannelForbidden
bot_id = int(TOKEN.split(":")[0])

if proxystart:
    client = TelegramClient("user", api_id, api_hash, proxy=proxy,
                            connection_retries=None).start()
else:
    client = TelegramClient("user", api_id, api_hash,
                            connection_retries=None).start()


DCs = [
    ["jd.com","京东服务器"],
    ["api.m.jd.com","京东(api)服务器"],
    ["lzdz1-isv.isvjcloud.com","京东(开卡)服务器"],
    ["jinggengjcq-isv.isvjcloud.com","京东(开卡2)服务器"],
    ["cjhydz-isv.isvjcloud.com","京东(组队cj)服务器"],
    ["lzkjdz-isv.isvjcloud.com","京东(组队lz)服务器"]
]



@client.on(events.NewMessage(pattern=r'^-pingjd$', outgoing=True))
@client.on(events.MessageEdited(pattern=r'^-pingjd$', outgoing=True))
async def pingjd(event):
    try:
        data = []
        for dc in DCs:
            result = await executes(f"ping -c 1 {dc[0]} | awk -F '/' " + "'END {print $5}'")
            data.append(result)
        res = ''
        for i in range(0, len(DCs)):
            res += f"{DCs[i][1]}: `{data[i] if 'ms' in data[i] else data[i]+'ms'}`\n"
        await event.edit(res)
        await asyncio.sleep(30)
        await event.delete()
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(pattern=r'^-pingjds$', outgoing=True))
@client.on(events.MessageEdited(pattern=r'^-pingjds$', outgoing=True))
async def pingjd(event):
    try:
        for n in range(1, 5):
            data = []
            for dc in DCs:
                result = await executes(f"ping -c 1 {dc[0]} | awk -F '/' " + "'END {print $5}'")
                data.append(result)
            res = ''
            for i in range(0, len(DCs)):
                res += f"{DCs[i][1]}: `{data[i] if 'ms' in data[i] else data[i]+'ms'}`\n"
            await event.edit(f"**第{n}次ping**\n\n"+res)
            await asyncio.sleep(2)
        await asyncio.sleep(10)
        await event.delete()
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")



@client.on(events.NewMessage(pattern=r'^-ping$', outgoing=True))
@client.on(events.MessageEdited(pattern=r'^-ping$', outgoing=True))
async def ping(event):
    try:
        """ 计算 bot 与 Telegram 之间的封包和信息延迟。 """
        start = datetime.now()
        await client(functions.PingRequest(ping_id=0))
        end = datetime.now()
        ping_duration = (end - start).microseconds / 1000
        start = datetime.now()
        await event.edit("Pong!")
        end = datetime.now()
        msg_duration = (end - start).microseconds / 1000
        await event.edit(f"Pong!| PING: {ping_duration} | MSG: {msg_duration}")
        await asyncio.sleep(20)
        await event.delete()

    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


async def executes(command, pass_error=True):
    """ 执行命令并返回输出，并选择启用stderr. """
    executor = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        stdout, stderr = await executor.communicate()
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
    if pass_error:
        result = str(stdout.decode().strip()) \
                 + str(stderr.decode().strip())
    else:
        result = str(stdout.decode().strip())
    return result







@client.on(events.NewMessage(chats=ql_log_bot,
                             pattern='.*萌宠.*|.*农场.*|.*工厂.*'))
async def 转发日记(event):
    try:
        message = event.message.text
        if 'cookie' not in message \
                and '异常' not in message and \
                '助力' not in message and \
                '重新' not in message and \
                '限制' not in message:
            if 'http' in message:
                tihuan = re.sub(r'htt.*', "学习", message)
                a = re.search(r'【京东账号(1{1})】|【京东账号(2{1})】', tihuan)
                if a:
                    b = re.sub(r"APP[\s\S]*", "", tihuan)
                    send_text_msg(user_id,
                                  tnanko, b)


            else:
                a = re.search(r'【京东账号(1{1})】|【京东账号(2{1})】', message)
                if a:
                    b = re.sub(r"APP[\s\S]*", "", message)
                    send_text_msg(user_id,
                                  tnanko, b)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(from_users=chat_id,pattern=r"^b\d*$|^c\d*$|^B\d*$|^C\d*$"))
async def get_bean(event):
    try:
        message = event.message.text
        for _bot in ql_bot:
            await client.send_message(_bot, '/bean 1')
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")







@client.on(events.NewMessage(chats=1716089227, pattern=r"/cmd.*"))
async def cmd_run(event):
    try:
        message = event.message.text
        if 'kill' not in message:
            with open('/ql/config/cmd.txt', 'r') as f1:
                a = f1.read()
            if message in a:
                return
            else:
                with open('/ql/config/cmd.txt', 'a+') as f1:
                    f1.write(message + '\n')
                for bot in ql_bot:
                    await client.send_message(bot, message)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")



@client.on(events.NewMessage(chats=ql_bot))
async def good_luck(event):
    try:
        message = event.message.text
        if '抽奖活动' in message:
            with open('/ql/scripts/wxid.txt', 'r') as f1:
                g = f1.read()
            b = re.findall('【京东账号.*】 获得.*', message)

            url = \
                re.findall('https://.*com/wxDrawActivity/.*',
                           message)[0]

            # 得到列表
            s = [s for s in b if
                 '积分' not in s and '券' not in s]
            print(s)

            # 开始遍历

            for all in s:
                try:
                    pin = re.findall('【京东账号(.*)】 获得', all)[0]
                    liwu = re.findall('【京东账号.*】 获得(.*)', all)[0]
                    wxid = re.findall(f'{pin}\$(.*)', g)[0]
                    print(url)
                    print(pin)
                    print(liwu)
                    print(wxid)
                    send_text_msg(user_id, wxid,
                                  '恭喜你' + pin + '\n获得：' + liwu + '\n领取的url：\n' + url)
                except Exception as e:
                    print(e)

            print(b, url)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(pattern=r'^re[ 0-9]*$|Re[ 0-9]*$',
                             outgoing=True))
async def 复制cp(event):
    num = event.raw_text.split(' ')
    if isinstance(num, list) and len(num) == 2:
        num = int(num[-1])
    else:
        num = 1
    reply = await event.get_reply_message()
    await event.delete()
    for _ in range(0, num):
        await reply.forward_to(int(event.chat_id))




@client.on(events.NewMessage(pattern=r'^id$', outgoing=True))
@client.on(events.MessageEdited(pattern=r'^id$', outgoing=True))
async def userid(event):
    """
    查询您回复的消息的发件人的 UserID
    """
    message = await event.get_reply_message()
    text = "Message ID: `" + str(event.message.id) + "`\n\n"
    text += "**Chat**\nid:`" + str(event.chat_id) + "`\n"
    msg_from = event.chat if event.chat else (await event.get_chat())
    if event.is_private:
        try:
            text += "first_name: `" + msg_from.first_name + "`\n"
        except TypeError:
            text += "**死号**\n"
        if msg_from.last_name:
            text += "last_name: `" + msg_from.last_name + "`\n"
        if msg_from.username:
            text += "username: @" + msg_from.username + "\n"
        if msg_from.lang_code:
            text += "lang_code: `" + msg_from.lang_code + "`\n"
    if event.is_group or event.is_channel:
        text += "title: `" + msg_from.title + "`\n"
        try:
            if msg_from.username:
                text += "username: @" + msg_from.username + "\n"
        except AttributeError:
            await event.edit('出错了呜呜呜 ~ 当前聊天似乎不是群聊。')
            return
        text += "date: `" + str(msg_from.date) + "`\n"
    if message:
        text += "\n" + '以下是被回复消息的信息' + "\nMessage ID: `" + str(message.id) + "`\n\n**User**\nid: `" + str(message.sender_id) + "`"
        try:
            if message.sender.bot:
                text += f"\nis_bot: 是"
            try:
                text += "\nfirst_name: `" + message.sender.first_name + "`"
            except TypeError:
                text += f"\n**死号**"
            if message.sender.last_name:
                text += "\nlast_name: `" + message.sender.last_name + "`"
            if message.sender.username:
                text += "\nusername: @" + message.sender.username
            if message.sender.lang_code:
                text += "\nlang_code: `" + message.sender.lang_code + "`"
        except AttributeError:
            pass
        if message.forward:
            if str(message.forward.chat_id).startswith('-100'):
                text += "\n\n**Forward From Channel**\nid: `" + str(
                    message.forward.chat_id) + "`\ntitle: `" + message.forward.chat.title + "`"
                if not isinstance(message.forward.chat, ChannelForbidden):
                    if message.forward.chat.username:
                        text += "\nusername: @" + message.forward.chat.username
                    text += "\nmessage_id: `" + str(message.forward.channel_post) + "`"
                    if message.forward.post_author:
                        text += "\npost_author: `" + message.forward.post_author + "`"
                    text += "\ndate: `" + str(message.forward.date) + "`"
            else:
                if message.forward.sender:
                    text += "\n\n**Forward From User**\nid: `" + str(
                        message.forward.sender_id) + "`"
                    try:
                        if message.forward.sender.bot:
                            text += f"\nis_bot: 是"
                        try:
                            text += "\nfirst_name: `" + message.forward.sender.first_name + "`"
                        except TypeError:
                            text += f"\n**死号**"
                        if message.forward.sender.last_name:
                            text += "\nlast_name: `" + message.forward.sender.last_name + "`"
                        if message.forward.sender.username:
                            text += "\nusername: @" + message.forward.sender.username
                        if message.forward.sender.lang_code:
                            text += "\nlang_code: `" + message.forward.sender.lang_code + "`"
                    except AttributeError:
                        pass
                    text += "\ndate: `" + str(message.forward.date) + "`"
    await event.edit(text)




@client.on(events.NewMessage(pattern=r'^d[ 0-9]*$|^D[ 0-9]*$',
                             outgoing=True))
async def delete_messages(event):
    try:
        num = event.raw_text.split(' ')
        if isinstance(num, list) and len(num) == 2:
            count = int(num[-1])
        else:
            count = 1
        await event.delete()
        count_buffer = 0
        async for message in client.iter_messages(event.chat_id,
                                                  from_user="me"):
            if count_buffer == count:
                break
            await message.delete()
            count_buffer += 1
        notification = await client.send_message(event.chat_id,
                                                 f'已删除{count_buffer}/{count}')
        time.sleep(.5)
        await notification.delete()
    except Exception as e:
        await client.send_message(event.chat_id, str(e))


# 监控高级user
@client.on(events.NewMessage(from_users=chat_id, pattern=r"^u$|^U$"))
async def user(event):
    try:
        message = event.message.text
        msg = await client.edit_message(event.chat_id,event.message.id, bot_name)
        await asyncio.sleep(1)
        await msg.delete()
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")



@client.on(events.NewMessage(from_users=chat_id, pattern=r"^重启$"))
async def reboot_bot(event):
    try:
        await client.send_message(event.chat_id, f"{bot_name}正在重启中...")
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


def mycron(lines):
    cronreg = re.compile(r'([0-9\-\*/,]{1,} ){4,5}([0-9\-\*/,]){1,}')
    return cronreg.search(lines).group()


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

@client.on(events.NewMessage(chats=myzdjr_chatIds))
async def huqun_id(event):
    try:
        message = event.message.text
        try:
            if is_Chinese(message):
                return
            if len(message) == 32 and message.isalnum:
                acid = message
                cmd = f'task gua_jointaem3 {acid}'
                with open('/ql/config/cmd.txt', 'r') as f1:
                    a = f1.read()
                if cmd in a:
                    return
                else:
                    with open('/ql/config/cmd.txt', 'a+') as f1:
                        f1.write(cmd + '\n')
                    for bot in ql_bot:
                        await client.send_message(bot, f'/cmd {cmd}')
                        await asyncio.sleep(20)
            elif "/cmd export guaopencard_actid=" in message:
                cmdtext = message
                with open('/ql/config/cmd.txt', 'r') as f1:
                    a = f1.read()
                if cmdtext in a:
                    return
                else:
                    with open('/ql/config/cmd.txt', 'a+') as f1:
                        f1.write(cmdtext + '\n')
                    for bot in ql_bot:
                        await client.send_message(bot, cmdtext)
                        await asyncio.sleep(20)
        except Exception as e:
            title = "【💥错误💥】"
            name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
            function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
            details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
            await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}")
            logger.error(f"错误--->{str(e)}")
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}")
        logger.error(f"错误--->{str(e)}")


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


@client.on(events.NewMessage(chats=ql_bot))
async def luck_draw(event):
    try:
        message = event.message.text
        if '抽奖活动' in message:
            with open('/ql/scripts/wxid.txt', 'r') as f1:
                g = f1.read()
            b = re.findall('【京东账号.*】 获得.*', message)

            url = \
                re.findall('https://.*com/wxDrawActivity/.*',
                           message)[0]
            s = [s for s in b if
                 '积分' not in s and '京豆' not in s and '券' not in s]
            print(s)
            for all in s:
                try:
                    pin = re.findall('【京东账号(.*)】 获得', all)[0]
                    liwu = re.findall('【京东账号.*】 获得(.*)', all)[0]
                    wxid = re.findall(f'{pin}\$(.*)', g)[0]
                    send_text_msg(user_id, wxid,
                                  '恭喜你' + pin + '\n获得：' + liwu + '\n领取的url：\n' + url)
                except Exception as e:
                    print(e)

            print(b, url)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
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
            end = bot_name
            write(configs)
            msg = await client.send_message(event.chat_id, end)
    except Exception as e:
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        await client.send_message(-1001690338060,
                                  f"「😡报错😡」\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{e}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage)
async def 收集脚本(event):
    try:
        if event.message.file:
            fname = event.message.file.name
            a = re.search(r'py$|js$|json$|sh$|exe$|zip$', fname)
            if a:
                await client.forward_messages(-1001578175826, event.message)
            else:
                return
        else:
            return
    except:
        return


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

@client.on(events.NewMessage(chats=myzdjr_chatIds,
                             pattern=r"^export jdjoyInvite_AllUrl=""=\".*\"|^export BirthGift_AllUrl=\".*\"|^export jd_smiek_package_activityUrl=\".*\"|^export pp_wxPointShopView_activityUrl=\".*\"|^export jd_smiek_luckDraw_activityUrl=\".*\"|^export jd_zdjr_.*=\".*\"|^export jd_smiek_addCart_activityUrl=\".*\"|^export jd_joinTeam_activityId.*=\".*\"|^export OPEN_CARD_.*=\".*\"|^export FAV_.*=\".*\"|^export ISV_.*=\".*\"|^export RUSH_LZCLIENT.*=\".*\""))
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
            await cmd(
                'task /ql/scripts/jd_open_card_by_shopid.js desi JD_COOKIE 1-15')
        elif "组队2" in identity:
            await cmd("task /ql/scripts/gua_joinTeam.js now")
        elif "收藏有礼" in identity:
            await cmd(
                'task /ql/scripts/jd_fav_shop_gift.js now desi JD_COOKIE 1-15')
        elif "关注有礼" in identity:
            await cmd(
                'task /ql/scripts/jspro_wxshop.js desi JD_COOKIE 1-15')
        elif "组队1" in identity:
            await cmd(
                "task /ql/scripts/gua_zdjr.js desi JD_COOKIE desi JD_COOKIE 1 4-40")
        elif "转盘抽奖" in identity:
            await cmd(
                "task /ql/scripts/rush_lzclient.js desi JD_COOKIE 1-15")
        elif "加购入会" in identity:
            await cmd(
                "task /ql/scripts/gua_addCart.js desi JD_COOKIE 1-15")
        elif "抽奖" in identity:
            await cmd(
                "task /ql/scripts/gua_luckDraw.js desi JD_COOKIE 1-15")
        elif "积分" in identity:
            await cmd(
                "task /ql/scripts/pp_wxPointShopView.js desi JD_COOKIE 1-10")
        elif "福袋" in identity:
            await cmd(
                "task /ql/scripts/jd_smiek_package.js desi JD_COOKIE 1-15")
        elif "生日" in identity:
            await cmd(
                "task /ql/scripts/jd_BirthGifts.js desi JD_COOKIE 1-15")
        elif "邀新" in identity:
            await cmd(
                "task /ql/scripts/gua_invite_join_shop.js")
        else:
            await jdbot.edit_message(msg, f"看到这行字,是有严重BUG!")
    except Exception as e:
        await jdbot.send_message(chat_id,
                                 'something wrong,I\'m sorry\n' + str(
                                     e))
        logger.error('something wrong,I\'m sorry\n' + str(e))



@client.on(events.NewMessage(chats=myzdjr_chatIds,
                             pattern=r'(export\s)?MyShopToken\d*=(".*"|\'.*\')'))  # 问号代表0次或1次
async def 店铺签到(event):
    try:
        messages = event.message.text.split("\n")
        exports = re.findall(r'export MyShopToken(\d+)="(.*)"',
                             rwcon("str"))  # 整个列表
        change, line, number = "", 0, 1
        if not exports:
            msg = await jdbot.send_message(chat_id,
                                           '监控到店铺签到环境变量，直接添加！')
            configs = rwcon("str")  # 读取整个config
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
        await client.send_message(-1001690338060,
                                  f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n报错行数：{str(e.__traceback__.tb_lineno)}行\n错误代码如下👇\n\n{message}")
        logger.error(f"错误--->{str(e)}")


gua_bot_id = 1891309600
group_id = -1001595416390  #找个机器人存在的群聊
forward_id = 1716089227  #拿到脚本转发哪里
@client.on(events.NewMessage(chats=[gua_bot_id]))
async def 搭讪保安(event):
    sender = await event.get_sender()
    message = await client.get_messages(sender.id, ids=event.message.id)
    gua_list = re.findall(r'KeyboardButtonCallback\(text=\'(.*?)\', data=b\'', str(message))
    if '请做出您的选择：' in str(message) and len(gua_list) != 0:
        if os.path.exists('gua_list.txt'):
            with open('gua_list.txt', 'r') as f1:
                g = f1.read()
            if '抽奖' not in gua_list[int(g)]:
                await message.click(text=gua_list[int(g)])
                await asyncio.sleep(10)
                if gua_list[int(g)] != '取消':
                    await client.send_message(gua_bot_id, "/getFile")
                    g = int(g) + 1
                    with open('gua_list.txt', 'w+') as f1:
                        f1.write(str(g))
                else:
                    with open('gua_list.txt', 'w+') as f1:
                        f1.write("0")
                    print('完成工作了。')
        else:
            with open('gua_list.txt', 'w+') as f1:
                f1.write("0")
    if event.message.file:
        await client.forward_messages(1716089227, event.message)  ##

@client.on(events.NewMessage(chats=group_id,pattern='我来拿脚本啦～'))
async def 拿脚本(event):
    await client.send_message(gua_bot_id, "/getFile")
    await client.send_message(-1001235868507, '签到领token')



