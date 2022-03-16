# NUIST_HealthyReport_NEW
可能是首个支持新版健康管理的Python自动填写工具，顺便支持了一下自动识别统一认证的验证码

新系统与东南大学的系统有部分相似，故本项目基于来自SEU的同学的GitHub项目：https://github.com/cogkitten/seu-daily-report 大量修改而来。

统一认证验证码在旧系统的自动填报脚本中就已成功识别，利用muggle_ocr解决了统一认证添加强制验证码的逻辑，可正常登陆填报

验证码识别基于南京大学校园网登陆脚本项目：https://github.com/cubiccm/NJU-Network-Authenticate

### 特别提醒

这里仅技术论证了健康日报的单次自动提交功能，一定程度上可以节约**身体健康的同学**填报健康日报的时间，但**请不要隐瞒自己的健康状况！**

**如果有特殊情况，请立即停用并修改当天记录为实际情况！**

**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**

### 使用前

如需要Server酱，请在135行、145行的api内填入你自己的Server酱SCT代码，就像下面一样。å

```python
api = "https://sctapi.ftqq.com/这里填写Server酱的SCT代码.send"
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
0 8 * * * python3 xxxx/report.py    # (模式一)
0 8 * * * python3 report.py -m manual -u xxx -p xxx     # (模式二)
```