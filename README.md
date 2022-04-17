<h1 align="center">
  Smell
  <br>
  Author: 喵喵喵
</h1>

## 服务器环境一键搭建

> 进入**服务器内以Root执行以下命令**，然后按提示操作即可

```shell
root=root; if [ -f $root/smell.sh ]; then rm -f $root/smell.sh; fi; cd $root; wget https://raw.githubusercontent.com/Charles-Hello/Study_Shell/master/smell.sh; bash smell.sh;
```

## Smell_Bot一键搭建

> 首先进入**docker容器内**执行以下命令，然后按提示操作即可

```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql;if [ -f $root/diybot.sh ]; then rm -f $root/diybot.sh; fi; cd $root; wget https://raw.githubusercontent.com/Charles-Hello/Study_Shell/master/diybot.sh; bash diybot.sh; fi
```

## 用户要求

- ~~🐶都会~~

## 常用命令

1. **重启程序**

```shell
if [ -d '/jd' ]; then cd /jd/jbot; pm2 start ecosystem.config.js; cd /jd; pm2 restart jbot; else ps -ef | grep 'python3 -m jbot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; nohup python3 -m jbot >/ql/log/bot/bot.log 2>&1 & fi 
```

## 配套QL辅助脚本

```shell
ql repo https://github.com/Charles-Hello/study_shell.git "miao_" "linux" "sh" 
```
