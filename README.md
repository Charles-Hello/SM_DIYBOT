<h1 align="center">
  Smell
  <br>
  Author: 喵喵喵
</h1>

## 目录
- [使用方式](#使用方式)
  - [一键搭建](#部署机器人)

- [常用命令](#常用命令)
# 仓库目录说明
```text
JD_Diy/                     # JD_Diy 仓库
  |-- config                    # 配置目录
  |-- jbot                      # 正式版机器人
  |-- requirements.txt          # 依赖文件
  `-- README.md                 # 仓库说明
```

## Smell一键搭建
首先进入容器中执行以下命令，然后按提示操作即可
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi; if [ -f $root/smell.sh ]; then rm -f $root/smell.sh; fi; cd $root; wget https://gentle-star-62f1.1140601003.workers.dev/https://raw.githubusercontent.com/Charles-Hello/study_shell/master/ql_tools/smell.sh; bash smell.sh
```

## 用户要求
- 会cv就好


## 部署方法
```shell
if [ -d "/jd" ]; then root=/jd; else root=/ql; fi; if [ -f $root/diybot.sh ]; then rm -f $root/diybot.sh; fi; cd $root; wget https://gentle-star-62f1.1140601003.workers.dev/https://raw.githubusercontent.com/Charles-Hello/study_shell/master/ql_tools/diybot.sh; bash diybot.sh;
```

1. 重启程序
```shell
if [ -d '/jd' ]; then cd /jd/jbot; pm2 start ecosystem.config.js; cd /jd; pm2 restart jbot; else ps -ef | grep 'python3 -m jbot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; nohup python3 -m jbot >/ql/log/bot/bot.log 2>&1 & fi 
```

