"""
要求：
    1、需要具备一定的 python3 知识；
    2、清楚自己需要编辑代码的区域；
    3、清楚自己需要导入的变量的位置和变量名。
"""


from .. import chat_id, jdbot, logger, api_id, api_hash, proxystart, proxy, _ConfigDir, _ScriptsDir, _OwnDir, _JdbotDir, _DiyScripts, _LogDir, _shortcut, _botlog, _botjson, img_file, _botset, _set, chname, TOKEN, StartCMD, proxyType, connectionType
from ..bot.utils import row, _CronFile, bean_log, _ConfigFile, V4, QL, _DiyDir, jdcmd, myck, split_list, backfile, press_event, cmd, getname, logbtn, logbtn, mycron, mycron, upcron, upcron, upcron, upcron, cronmanger, cronmanger
from telethon import events, Button
from asyncio import exceptions


"""
如果需要导入 diy 目录内某个文件的变量或函数
from ..diy.xxx import xxx
例如：from ..diy.utils import ql_token
"""

"""
如果需要导入 bot 目录内某个文件的变量或函数
from ..bot.xxx import xxx
例如：from ..bot.utils import myck
"""


"""
如果需要导入其他第三方库
import xxx
例如：import json
"""


async def smiek_jd_zdjr():
    try:
        await cmd("task /ql/scripts/smiek_jd_zdjr.js now && task /ql/scripts/smiek_jd_zdjr.js now") # 组队瓜分京豆团ID更新后自动执行smiek_jd_zdjr.js脚本

    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def jd_joinTeam_activityId():
    try:
        await cmd("task /ql/scripts/gua_joinTeam.js now && task /ql/scripts/gua_joinTeam.js now") # 组队瓜分京豆2222团ID更新后自动执行gua_joinTeam.js脚本

    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

async def jd_open_card_by_shopid():
    try:
        await cmd("task /ql/scripts/jd_open_card_by_shopid.js now") # 入会开卡ID更新后自动执行jd_open_card_by_shopid.js脚本 脚本绝对路径 now

    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
        
async def jd_fav_shop_gift():
    try:
        await cmd("task /ql/scripts/jd_fav_shop_gift.js now") # 收藏有礼ID更新后自动执行jd_fav_shop_gift.js脚本 脚本绝对路径 now

    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
        
async def jd_follow_wxshop_gift():
    try:
        await cmd("task /ql/scripts/jd_follow_wxshop_gift_lof.js now") # 关注有礼ID更新后自动执行jd_follow_wxshop_gift_lof.js脚本 脚本绝对路径 now

    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def getcookie(jd_cookie):
    try:
        """
        try 部分则自由发挥即可
        jd_cookie 是传入的 cookie 具体值
        """








    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))