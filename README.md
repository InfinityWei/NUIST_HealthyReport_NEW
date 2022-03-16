# NUIST_HealthyReport_NEW
可能是首个支持新版健康管理的Python自动填写工具，顺便支持识别统一认证的验证码

新系统与东南大学的系统有部分相似，故本项目基于来自SEU的同学的GitHub项目：https://github.com/cogkitten/seu-daily-report 大量修改而来。

统一认证验证码在旧系统的自动填报脚本中就已成功识别，利用muggle_ocr解决了统一认证添加强制验证码的逻辑，可正常登陆填报

验证码识别基于南京大学校园网登陆脚本项目：https://github.com/cubiccm/NJU-Network-Authenticate

### 特别提醒

这里仅技术论证了健康日报的单次自动提交功能，一定程度上可以节约**身体健康的同学**填报健康日报的时间，但**请不要隐瞒自己的健康状况！**

**如果有特殊情况，请立即停用并修改当天记录为实际情况！**

**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**

### 使用前

如不需要Server酱的填写情况推送服务，请将从137行到144行、从147行到154行的代码删去，如需要，请在143行、153行的api内填入你自己的Server酱SCT代码，就像下面一样。

```python
api = "https://sctapi.ftqq.com/这里填写Server酱的SCT代码.send"
```

### Windows系统

系统需安装好Python3.8以上，pip

CMD或者PowerShell进入目录

```powershell
cd E:\Desktop\DailyHealthReport
```

安装Python依赖，需要的依赖都已经列在requirements.txt里

```powershell
pip install -r requirements.txt
```

py运行run.py文件

```powershell
python report.py 学号 信息门户密码
```

### Linux系统

Linux系统比较类似，注意Python版本需要3.8以上，否则可能无法正常使用tensorflow，造成验证码无法解决。



**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**
