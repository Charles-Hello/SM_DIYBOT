from telethon import TelegramClient, connection
import json
import os
import logging

_JdDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_ConfigDir = f'{_JdDir}/config'
_ScriptsDir = f'{_JdDir}/scripts'
_OwnDir = f'{_JdDir}/own'
_JdbotDir = f'{_JdDir}/jbot'
_DiyScripts = f'{_JdDir}/diyscripts'
_LogDir = f'{_JdDir}/log'
_shortcut = f'{_ConfigDir}/shortcut.list'
_botlog = f'{_LogDir}/bot/run.log'
_botjson = f'{_ConfigDir}/bot.json'
img_file = f'{_ConfigDir}/qr.jpg'
_botset = f'{_ConfigDir}/botset.json'
_set = f'{_JdbotDir}/set.json'
QR_IMG_FILE = f'{_ConfigDir}/qr.jpg'
if not os.path.exists(f'{_LogDir}/bot'):
    os.mkdir(f'{_LogDir}/bot')
logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename=_botlog,
    filemode='w')
logger = logging.getLogger(__name__)
if os.path.exists(_botjson):
    with open(_botjson, 'r', encoding='utf-8') as f:
        bot = json.load(f)
if os.path.exists(_botset):
    with open(_botset, 'r', encoding='utf-8') as f:
        mybot = json.load(f)
else:
    with open(_set, 'r', encoding='utf-8') as f:
        mybot = json.load(f)
if '开启别名' in mybot.keys() and mybot['开启别名'].lower() == 'true':
    chname = True
else:
    chname = False
chat_id = int(bot['user_id'])
# 机器人 TOKEN
TOKEN = bot['bot_token']
# HOSTAPI = bot['apihost']
# 发消息的TG代理
# my.telegram.org申请到的api_id,api_hash
api_id = bot['api_id']
api_hash = bot['api_hash']
proxystart = bot['proxy']
StartCMD = bot['StartCMD']
proxyType = bot['proxy_type']
connectionType = connection.ConnectionTcpMTProxyRandomizedIntermediate if proxyType == "MTProxy" else connection.ConnectionTcpFull
if 'proxy_user' in bot.keys() and bot['proxy_user'] != "代理的username,有则填写，无则不用动":
    proxy = {
        'proxy_type': bot['proxy_type'],
        'addr':  bot['proxy_add'],
        'port': bot['proxy_port'],
        'username': bot['proxy_user'],
        'password': bot['proxy_password']}
elif proxyType == "MTProxy":
    proxy = (bot['proxy_add'], bot['proxy_port'], bot['proxy_secret'])
else:
    proxy = (bot['proxy_type'], bot['proxy_add'], bot['proxy_port'])
# 开启tg对话
if proxystart and 'noretry' in bot.keys() and bot['noretry']:
    jdbot = TelegramClient('bot', api_id, api_hash, connection=connectionType,
                           proxy=proxy).start(bot_token=TOKEN)
elif proxystart:
    jdbot = TelegramClient('bot', api_id, api_hash, connection=connectionType,
                           proxy=proxy, connection_retries=None).start(bot_token=TOKEN)
elif 'noretry' in bot.keys() and bot['noretry']:
    jdbot = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)
else:
    jdbot = TelegramClient('bot', api_id, api_hash,
                           connection_retries=None).start(bot_token=TOKEN)
