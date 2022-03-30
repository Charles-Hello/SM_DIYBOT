#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
import re
import sys
import time
from asyncio import exceptions

import requests
from telethon import events, Button

from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import press_event, V4, _ConfigFile, row, split_list, _Auth, myck
from ..diy.utils import QL8, ql_token, rwcon

bot_id = int(TOKEN.split(":")[0])


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/blockcookie'))
async def mytempblockcookie(event):
    try:
        sender = event.sender_id
        message = event.message.raw_text
        ck_num = message.replace("/blockcookie", "")
        goon = True
        if len(ck_num) <= 1:
            while goon:
                if V4:
                    goon = await v4_block(sender)
                else:
                    goon = await ql_block(sender)
        elif ck_num.replace(" ", "").isdigit():
            if V4:
                await v4_appoint(ck_num.replace(" ", ""))
            else:
                await ql_appoint(ck_num.replace(" ", ""))
        elif not ck_num.replace(" ", "").isdigit():
            await jdbot.send_message(chat_id, "非法输入！参考下面所给实例进行操作！\n/blockcookie 1（屏蔽账号1）")
    except Exception as e:
        title = "【💥错误💥】"
        name = sys.argv[0].split("/")[-1].split(".")[0]
        function = sys._getframe().f_code.co_name
        await jdbot.send_message(chat_id, f"{title}\n\n文件名：{name}\n函数名：{function}\n错误原因：{str(e)}\n\n建议百度/谷歌查询")
        logger.error(f"错误--->{str(e)}")


async def v4_block(sender):
    try:
        async with jdbot.conversation(sender, timeout=120) as conv:
            msg = await conv.send_message("请做出您的选择")
            buttons = [
                Button.inline("查询目前屏蔽", data="inquire"),
                Button.inline("指定屏蔽账号", data="designated block"),
                Button.inline("指定取消屏蔽", data="designated unblock"),
                Button.inline("取消所有屏蔽", data="unblock all accounts"),
                Button.inline('取消会话', data='cancel')
            ]
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(buttons, row))
            convdata = await conv.wait_event(press_event(sender))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.edit_message(msg, '对话已取消')
                return False
            else:
                with open(_ConfigFile, 'r', encoding='utf-8') as f1:
                    configs = f1.readlines()
                for config in configs:
                    if "TempBlockCookie" in config and " TempBlockCookie" not in config and "举例" not in config:
                        line = configs.index(config)
                        blocks = re.findall(r'"([^"]*)"', config)[0]
                        if len(blocks) == 0:
                            blocks = []
                        elif " " in blocks:
                            blocks = list(map(int, blocks.split(" ")))
                        else:
                            blocks = [int(blocks)]
                        break
                    elif "AutoDelCron" in config:
                        await jdbot.edit_message(msg, "无法找到 TempBlockCookie 目标字符串，请检查是否使用了标准配置模板")
                        return False
                if res == 'inquire':
                    message = f"目前的屏蔽情况是：\n{str(' '.join('%s' % _ for _ in sorted(blocks, reverse=False))) if len(blocks) != 0 else '没有帐号被屏蔽'}"
                    return await operate(conv, sender, msg, message)
                elif res == 'designated block':
                    acounts = len(myck(_ConfigFile)[0])
                    if acounts == len(blocks):
                        message = "所有账号都已被屏蔽，无需继续屏蔽"
                        return await operate(conv, sender, msg, message)
                    cks, btns = [], []
                    for i in range(acounts):
                        cks.append(i + 1)
                    btns_list = list(set(cks) - set(blocks))
                    btns_list.sort()
                    for block in btns_list:
                        btn = Button.inline(f"账号{str(block)}", data=block)
                        btns.append(btn)
                    btns.append(Button.inline("上级菜单", data="upper menu"))
                    btns.append(Button.inline('取消会话', data='cancel'))
                    msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(btns, row))
                    convdata = await conv.wait_event(press_event(sender))
                    res_2 = bytes.decode(convdata.data)
                    if res_2 == 'upper menu':
                        await jdbot.delete_messages(chat_id, msg)
                        return True
                    elif res_2 == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        return False
                    else:
                        blocks.append(int(res_2))
                        blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
                        configs[line] = f'TempBlockCookie="{blocks}"\n'
                        with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                            f2.write(''.join(configs))
                        message = f"指定屏蔽账号{str(res_2)}成功"
                        return await operate(conv, sender, msg, message)
                elif res == 'designated unblock':
                    if not blocks:
                        message = "没有账号被屏蔽，无需取消屏蔽"
                        return await operate(conv, sender, msg, message)
                    btns = []
                    for block in blocks:
                        btn = Button.inline(f"账号{str(block)}", data=block)
                        btns.append(btn)
                    btns.append(Button.inline("上级菜单", data="upper menu"))
                    btns.append(Button.inline('取消会话', data='cancel'))
                    msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(btns, row))
                    convdata = await conv.wait_event(press_event(sender))
                    res_2 = bytes.decode(convdata.data)
                    if res_2 == 'upper menu':
                        await jdbot.delete_messages(chat_id, msg)
                        return True
                    elif res_2 == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        return False
                    else:
                        blocks.remove(int(res_2))
                        blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
                        configs[line] = f'TempBlockCookie="{blocks}"\n'
                        with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                            f2.write(''.join(configs))
                        message = f"指定取消屏蔽账号{res_2}成功"
                        return await operate(conv, sender, msg, message)
                elif res == 'unblock all accounts':
                    configs[line] = 'TempBlockCookie=""\n'
                    with open(_ConfigFile, 'w', encoding='utf-8') as f2:
                        f2.write(''.join(configs))
                    message = "取消屏蔽所有账号成功"
                    return await operate(conv, sender, msg, message)
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
        return False


async def ql_block(sender):
    try:
        async with jdbot.conversation(sender, timeout=120) as conv:
            msg = await conv.send_message("请做出您的选择")
            buttons = [
                Button.inline("查询启停状态", data="query start and stop status"),
                Button.inline("指定启用账号", data="specify to able an account"),
                Button.inline("指定禁用账号", data="specify to disable an account"),
                Button.inline("启用全部账号", data="enable all accounts"),
                Button.inline("禁用全部账号", data="disable all accounts"),
                Button.inline('取消会话', data='cancel')
            ]
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(buttons, row))
            convdata = await conv.wait_event(press_event(sender))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.edit_message(msg, '对话已取消')
                return False
            else:
                with open(_Auth, 'r', encoding='utf-8') as f:
                    auth = json.load(f)
                token = auth['token']
                headers = {'Authorization': f'Bearer {token}'}
                cookiedatas = []
                try:
                    ql_version = '2.2'
                    url = 'http://127.0.0.1:5600/api/cookies'
                    body = {'t': int(round(time.time() * 1000))}
                    datas = requests.get(url, params=body, headers=headers).json()['data']
                    for data in datas:
                        cknum = datas.index(data) + 1
                        cookie = data['value']
                        remarks = data['nickname']
                        status = data['status']
                        _id = data['_id']
                        cookiedatas.append([cknum, cookie, remarks, status, _id])
                except:
                    ql_version = '2.8+'
                    url = 'http://127.0.0.1:5600/api/envs'
                    body = {
                        'searchValue': 'JD_COOKIE',
                        'Authorization': f'Bearer {token}'
                    }
                    datas = requests.get(url, params=body, headers=headers).json()['data']
                    for data in datas:
                        cookiedatas.append([datas.index(data) + 1, data['value'], data['remarks'] if 'remarks' in data.keys() else "未备注", '启用' if data['status'] == 0 else '禁用', data['_id']])
                if res == 'query start and stop status':
                    message = "目前启停状态\n\n"
                    for cookiedata in cookiedatas:
                        message += f'账号{cookiedata[0]}\n备注：{cookiedata[2]}\n启停状态：{cookiedata[3]}\n\n'
                    return await operate(conv, sender, msg, message)
                elif res == 'specify to able an account' or res == 'specify to disable an account':
                    btns = []
                    if "disable" in res:
                        for cookiedata in cookiedatas:
                            if cookiedata[3] == '启用':
                                btn = Button.inline(f"账号{cookiedata[0]}", data=cookiedata[4])
                                btns.append(btn)
                        if not btns:
                            return await operate(conv, sender, msg, '没有账号被启用，无法禁用账号')
                    else:
                        for cookiedata in cookiedatas:
                            if cookiedata[3] == '禁用':
                                btn = Button.inline(f"账号{cookiedata[0]}", data=cookiedata[4])
                                btns.append(btn)
                        if not btns:
                            return await operate(conv, sender, msg, '没有账号被禁用，无需启用账号')
                    btns.append(Button.inline("上级菜单", data="upper menu"))
                    btns.append(Button.inline('取消会话', data='cancel'))
                    msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=split_list(btns, row))
                    convdata = await conv.wait_event(press_event(sender))
                    res_2 = bytes.decode(convdata.data)
                    if res_2 == 'upper menu':
                        await jdbot.delete_messages(chat_id, msg)
                        return True
                    elif res_2 == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        return False
                    else:
                        if "disable" in res:
                            if ql_version == '2.2':
                                url = 'http://127.0.0.1:5600/api/cookies/disable'
                            else:
                                url = 'http://127.0.0.1:5600/api/envs/disable'
                            body = [f"{res_2}"]
                            r = requests.put(url, json=body, headers=headers)
                            if r.ok:
                                return await operate(conv, sender, msg, '禁用成功')
                            else:
                                return await operate(conv, sender, msg, '禁用失败，请手动禁用')
                        else:
                            if ql_version == '2.2':
                                url = 'http://127.0.0.1:5600/api/cookies/enable'
                            else:
                                url = 'http://127.0.0.1:5600/api/envs/enable'
                            body = [f"{res_2}"]
                            r = requests.put(url, json=body, headers=headers)
                            if r.ok:
                                return await operate(conv, sender, msg, '启用成功')
                            else:
                                return await operate(conv, sender, msg, '启用失败，请手动启用')
                else:
                    _ids = []
                    if "disable" in res:
                        for cookiedata in cookiedatas:
                            if cookiedata[3] == '启用':
                                _ids.append([cookiedata[0], cookiedata[4]])
                        if not _ids:
                            return await operate(conv, sender, msg, '没有账号被启用，无法禁用全部账号')
                    else:
                        for cookiedata in cookiedatas:
                            if cookiedata[3] == '禁用':
                                _ids.append([cookiedata[0], cookiedata[4]])
                        if not _ids:
                            return await operate(conv, sender, msg, '没有账号被禁用，无需启用全部账号')
                    if "disable" in res:
                        if ql_version == '2.2':
                            url = 'http://127.0.0.1:5600/api/cookies/disable'
                        else:
                            url = 'http://127.0.0.1:5600/api/envs/disable'
                    else:
                        if ql_version == '2.2':
                            url = 'http://127.0.0.1:5600/api/cookies/enable'
                        else:
                            url = 'http://127.0.0.1:5600/api/envs/enable'
                    message = ""
                    if "disable" in res:
                        for _id in _ids:
                            body = [f"{_id[-1]}"]
                            r = requests.put(url, json=body, headers=headers)
                            if r.ok:
                                message += f"账号{_id[0]}禁用成功\n"
                            else:
                                message += f"账号{_id[0]}禁用失败，请手动禁用\n"
                        return await operate(conv, sender, msg, message)
                    else:
                        for _id in _ids:
                            body = [f"{_id[-1]}"]
                            r = requests.put(url, json=body, headers=headers)
                            if r.ok:
                                message += f"账号{_id[0]}启用成功\n"
                            else:
                                message += f"账号{_id[0]}启用失败，请手动启用\n"
                        return await operate(conv, sender, msg, message)
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
        return False


async def v4_appoint(ck_num):
    msg = await jdbot.send_message(chat_id, f"开始屏蔽账号{ck_num}")
    with open(_ConfigFile, 'r', encoding='utf-8') as f1:
        configs = f1.readlines()
    for config in configs:
        if "TempBlockCookie" in config and " TempBlockCookie" not in config and "举例" not in config:
            line = configs.index(config)
            blocks = re.findall(r'"([^"]*)"', config)[0]
            if len(blocks) == 0:
                blocks = []
            elif " " in blocks:
                blocks = list(map(int, blocks.split(" ")))
            else:
                blocks = [int(blocks)]
            break
        elif "AutoDelCron" in config:
            await jdbot.edit_message(msg, "无法找到 TempBlockCookie 目标字符串，请检查是否使用了标准配置模板")
            return
    if int(ck_num) in blocks:
        await jdbot.edit_message(msg, f"账号{str(ck_num)}已经被屏蔽，无需再次屏蔽")
        return
    blocks.append(int(ck_num))
    blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
    configs[line] = f'TempBlockCookie="{blocks}"\n'
    with open(_ConfigFile, 'w', encoding='utf-8') as f2:
        f2.write(''.join(configs))
    await jdbot.edit_message(msg, f"指定屏蔽账号{str(ck_num)}成功")


async def ql_appoint(ck_num):
    msg = await jdbot.send_message(chat_id, f"开始屏蔽账号{ck_num}")
    with open(_Auth, 'r', encoding='utf-8') as f:
        auth = json.load(f)
    token = auth['token']
    headers = {'Authorization': f'Bearer {token}'}
    cookiedatas = []
    try:
        ql_version = '2.2'
        url = 'http://127.0.0.1:5600/api/cookies'
        body = {'t': int(round(time.time() * 1000))}
        datas = requests.get(url, params=body, headers=headers).json()['data']
        for data in datas:
            cookiedatas.append([datas.index(data) + 1, data['_id']])
    except:
        ql_version = '2.8+'
        url = 'http://127.0.0.1:5600/api/envs'
        body = {
            'searchValue': 'JD_COOKIE',
            'Authorization': f'Bearer {token}'
        }
        datas = requests.get(url, params=body, headers=headers).json()['data']
        for data in datas:
            cookiedatas.append([datas.index(data) + 1, data['_id']])
    if len(cookiedatas) < int(ck_num):
        await jdbot.edit_message(msg, f"无法找到账号{ck_num}的信息，禁用失败")
        return
    if ql_version == '2.2':
        url = 'http://127.0.0.1:5600/api/cookies/disable'
    else:
        url = 'http://127.0.0.1:5600/api/envs/disable'
    body = [f"{cookiedatas[int(ck_num) - 1][1]}"]
    r = requests.put(url, json=body, headers=headers)
    if r.ok:
        await jdbot.edit_message(msg, f"指定禁用账号{ck_num}成功")
    else:
        await jdbot.edit_message(msg, f"指定禁用账号{ck_num}失败，请手动禁用")


async def operate(conv, sender, msg, message):
    buttons = [
        Button.inline("上级菜单", data="upper menu"),
        Button.inline('取消会话', data='cancel')
    ]
    msg = await jdbot.edit_message(msg, message, buttons=split_list(buttons, row))
    convdata = await conv.wait_event(press_event(sender))
    res = bytes.decode(convdata.data)
    if res == 'upper menu':
        await jdbot.delete_messages(chat_id, msg)
        return True
    else:
        await jdbot.edit_message(msg, '对话已取消')


@jdbot.on(events.NewMessage(from_users=bot_id, pattern=r'.*cookie已失效.*'))
async def myautoblock(event):
    try:
        message = event.message.text.replace("\n", "")
        pt_pin = re.findall("cookie已失效.*京东账号\d+\s(.*)请.*", message)
        if not pt_pin and ("jd" in pt_pin or "%" in pt_pin):
            return
        msg = await jdbot.send_message(chat_id, "侦测到cookie失效通知，开始屏蔽账号")
        pt_pin = pt_pin[0]
        line, expired, blocks = None, None, []
        if V4:
            configs = rwcon("list")
            for config in configs:
                if pt_pin in config and "wskey" not in config:
                    expired = int(re.findall(r"[Cc]ookie(\d+)=.*", config)[0])
                    line = configs.index(config)
                    break
                elif "第二区域" in config:
                    await jdbot.edit_message(msg, f"无法寻找到{pt_pin}段的cookie存在于配置中！")
                    return
            for config in configs[line:]:
                if "TempBlockCookie" in config and " TempBlockCookie" not in config and "举例" not in config and ";;" not in configs[configs.index(config) + 1]:
                    line = configs.index(config)
                    blocks = re.findall(r'"([^"]*)"', config)[0]
                    if len(blocks) == 0:
                        blocks = []
                    elif " " in blocks:
                        blocks = list(map(int, blocks.split(" ")))
                    else:
                        blocks = [int(blocks)]
                    break
                elif "AutoDelCron" in config:
                    await jdbot.edit_message(msg, "无法找到 TempBlockCookie 目标字符串，请检查是否使用了标准配置模板")
                    return
            if expired in blocks:
                await jdbot.edit_message(msg, f"【取消】{pt_pin}先前已经被屏蔽，因此取消屏蔽！")
            else:
                blocks.append(expired)
                blocks = " ".join('%s' % _ for _ in sorted(blocks, reverse=False))
                configs[line] = f'TempBlockCookie="{blocks}"\n'
                rwcon(configs)
                await jdbot.edit_message(msg, f"【成功】{pt_pin}屏蔽成功！")
        elif QL8:
            token = ql_token(_Auth)
            url = 'http://127.0.0.1:5600/api/envs'
            headers = {'Authorization': f'Bearer {token}'}
            body = {"searchValue": f";pt_pin={pt_pin};"}
            datas = requests.get(url, headers=headers, json=body).json()['data']
            for data in datas:
                if pt_pin in data['value'] and "pt_key" in data['value']:
                    url = 'http://127.0.0.1:5600/api/envs/disable'
                    requests.put(url, headers=headers, json=[data['_id']])
                    await jdbot.edit_message(msg, f"【成功】{pt_pin}屏蔽成功！")
                    break
        else:
            token = ql_token(_Auth)
            url = 'http://127.0.0.1:5600/api/cookies'
            headers = {'Authorization': f'Bearer {token}'}
            datas = requests.get(url, headers=headers).json()['data']
            for data in datas:
                if pt_pin in data['value'] and "pt_key" in data['value']:
                    url = 'http://127.0.0.1:5600/api/cookies/disable'
                    requests.put(url, headers=headers, json=[data['_id']])
                    await jdbot.edit_message(msg, f"【成功】{pt_pin}屏蔽成功！")
                    break
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
