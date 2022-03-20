# NUIST_HealthyReport_NEW
可能是首个支持新版健康管理的Python自动填写工具，顺便支持了一下自动识别统一认证的验证码

新系统与东南大学的系统有部分相似，故本项目基于来自SEU的同学的GitHub项目：https://github.com/cogkitten/seu-daily-report 大量修改而来。

统一认证验证码在旧系统的自动填报脚本中就已成功识别，利用muggle_ocr解决了统一认证添加强制验证码的逻辑，可正常登陆填报

验证码识别基于南京大学校园网登陆脚本项目：https://github.com/cubiccm/NJU-Network-Authenticate

### 特别提醒

这里仅技术论证了健康日报的单次自动提交功能，一定程度上可以节约**身体健康的同学**填报健康日报的时间，但**请不要隐瞒自己的健康状况！**

**如果有特殊情况，请立即停用并修改当天记录为实际情况！**

**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**

---

### 可选参数
```
usage: report.py [-h] [-m MODE] [-u USERNAME] [-p PASSWORD] [-b BARK] [-k KEY] [-t TITLE] [-c CONTENT]
[-s SERVER_SCT]

-h, --help            show this help message and exit
  -m MODE, --mode MODE  用户名/密码读取方式。file选项为读取当前目录下user_data.json, manual选项为手动填写。默认为file模式
  -u USERNAME, --username USERNAME
                        一卡通/校园门户用户名，默认为学号
  -p PASSWORD, --password PASSWORD
                        一卡通/校园门户密码
  -b BARK, --bark BARK  是否开启Bark推送,默认为F。可选T/F
  -k KEY, --key KEY     Bark推送的个人API
  -t TITLE, --title TITLE
                        Bark推送标题,默认为"健康日报"。仅在Bark推送开启时奏效
  -c CONTENT, --content CONTENT
                        Bark推送正文。仅在Bark推送开启时奏效
  -s SERVER_SCT, --server_sct SERVER_SCT
                        Server酱推送SCT码
```
使用样例
```
python3 report.py
使用配置文件读取登陆信息，且不使用推送功能

python3 report.py -m manual -u 2020xxxxxxxx -p xxxxxxxxx
不读取配置文件，使用手动输入用户名密码的方式登陆

python3 report.py -m manual -u 2020xxxxxxxx -p xxxxxxxxx -b T -k Sdxwo9xxxxxxx -c xxx用户已打卡成功
使用手动方式登陆，并使用bark推送服务

python3 report.py -m manual -u 2020xxxxxxxx -p xxxxxxxxx -s xxxxxxxx
使用Server酱推送
```

---

### 使用方式
> 建议Python版本 >= 3.8

```
git clone https://github.com/InfinityWei/NUIST_HealthyReport_NEW.git
cd NUIST_HealthyReport_NEW  
pip3 install -r requirements.txt
```
登陆方式有两种，但推荐使用第一种(配置文件登陆)，不会在terminal留下history,且每次运行无需重复输入账号密码。  

---

#### 方式一(推荐)
填写`user_data.json`文件
```json
{
    "username":"xxx",
    "password":"xxx"
}
```
直接运行
```
python3 report.py
```

---
#### 方式二(不推荐)
在命令中加入账号密码
```
python3 -m manual -u xxxx -p xxxx
```

---

### 自动化运行

> 另外注意，Linux环境下可能需要nodejs环境
> yum install epel-release
> yum install nodejs

在服务器上设定定时任务，以每天定时执行
```
crontab -e
```
键入如下命令(每天早上8点运行)
```
# 后台运行，并将结果输出至out.file
0 8 * * * python3 report.py -b T -k Sdxwo9xxxxxxx -c xxx用户已打卡成功 > out.file 2>&1 &
```
---

### 效果图
![](pic/help.png)
![](pic/command.png)
![](pic/bark.png)