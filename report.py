#!/usr/bin/python3
from __future__ import print_function
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import execjs
import os
import re
import random
import hashlib
import argparse
import json


def login(sess, uname, pwd):
    login_url = 'https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fi.nuist.edu.cn%2Fqljfwapp%2Fsys%2FlwNuistHealthInfoDailyClock%2Findex.do%23%2FhealthClock'
    r = sess.get(login_url, timeout=5)
    htmlTextOri = r.text
    html = BeautifulSoup(htmlTextOri, 'lxml')
    pwdEncryptSalt = html.find(id='pwdEncryptSalt')['value']
    execution = html.find(id='execution')['value']
    with open('./encrypt.js', 'r', encoding="utf-8") as f:
         script = f.read()
    encrypt = execjs.compile(script)
    password = encrypt.call(
         '_ep', pwd, pwdEncryptSalt)
    
    
    personal_info = {'username': uname,
                     'password': password,
                     'captcha': '',
                     'lt': '',
                     'cllt': 'userNameLogin',
                     'execution': execution,
                     '_eventId': 'submit',
                     }
    r = requests.get("https://authserver.nuist.edu.cn/authserver/checkNeedCaptcha.htl?username=" + uname)
    if r.text == '{"isNeed":true}':
       print("CAPTCHA required")
       print("Initializing OCR...")
       import muggle_ocr
       os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'
       print("Obtaining CAPTCHA...")
       res = sess.get("https://authserver.nuist.edu.cn/authserver/getCaptcha.htl")
       print("Solving CAPTCHA...")
       sdk = muggle_ocr.SDK(model_type = muggle_ocr.ModelType.Captcha)
       captcha_text = sdk.predict(image_bytes = res.content)
       print("CAPTCHA:", captcha_text)
       personal_info["captcha"] = captcha_text
       global captcha
       captcha = captcha_text
       print("Logging in...")
    login_response = sess.post(login_url, personal_info)
    login_response.encoding = 'utf-8'
    if re.search("学院", login_response.text):
        print("\033[32m登陆成功!\033[01m")
    elif re.search("书院", login_response.text):
        print("\033[32m登陆成功!\033[01m")
    else:
        print("\033[31m登陆失败!请检查一卡通号和密码。\033[01m")
        raise


def get_header(sess, cookie_url):
    cookie_response = sess.get(cookie_url)
    weu = requests.utils.dict_from_cookiejar(cookie_response.cookies)['_WEU']
    cookie = requests.utils.dict_from_cookiejar(sess.cookies)

    header = {'Referer': 'http://i.nuist.edu.cn/qljfwapp/sys/lwNuistHealthInfoDailyClock/index.do#/healthClock',
              'Cookie': '_WEU=' + weu + '; MOD_AUTH_CAS=' + cookie['MOD_AUTH_CAS'] + ';'}
    return header


def get_info(sess, header):
    info_url = 'http://i.nuist.edu.cn/qljfwapp/sys/lwNuistHealthInfoDailyClock/modules/healthClock/getMyDailyReportDatas.do'
    info_response = sess.post(info_url, data={'pageSize': '10', 'pageNumber': '1'}, headers=header)
    return info_response


def report(sess,sct):
    try:
        cookie_url = 'http://i.nuist.edu.cn/qljfwapp/sys/lwNuistHealthInfoDailyClock/configSet/noraml/getRouteConfig.do'
        header = get_header(sess, cookie_url)
        info = get_info(sess, header)
        if info.status_code == 403:
            raise
    except:
        cookie_url2 = 'http://i.nuist.edu.cn/qljfwapp/sys/lwpub/api/getServerTime.do'
        header = get_header(sess, cookie_url2)
        info = get_info(sess, header)
    
    if info.status_code == 200:
        print('\033[32m获取前一日信息成功！\033[01m')
    else:
        print("\033[31m获取信息失败！\033[01m")
        raise
    info.encoding = 'utf-8'
    raw_info = re.search('"rows":\[\{(.*?)}', info.text).group(1)
    raw_info = raw_info.split(',')
    post_key = ['BY6', 'BY5', 'BY4', 'BY3', 'TODAY_ISOLATE_CONDITION', 'BY2', 'BY1', 'TODAY_CONDITION', 'BY2_DISPLAY', 'TODAY_BODY_CONDITION', 'TODAY_HEALTH_CODE_DISPLAY', 'CONTACT_HISTORY', 'TODAY_HEALTH_CODE', 'BY4_DISPLAY', 'TODAY_TARRY_CONDITION_DISPLAY', 'BY3_DISPLAY', 'PHONE_NUMBER', 'BY14', 'BY15', 'BY12', 'BY13', 'BY18', 'BY19', 'CHECKED_DISPLAY', 'BY16', 'BY17', 'TODAY_TEMPERATURE', 'CZRQ', 'BY10', 'BY11', 'BY8_DISPLAY', 'TODAY_TARRY_CONDITION', 'CLOCK_SITUATION', 'WID', 'TODAY_NAT_CONDITION', 'TODAY_VACCINE_CONDITION_DISPLAY', 'DEPT_NAME', 'CONTACT_HISTORY_DISPLAY', 'CZR', 'TODAY_CONDITION_DISPLAY', 'BY1_DISPLAY', 'TODAY_SITUATION_DISPLAY', 'CZZXM', 'BY20', 'TODAY_ISOLATE_CONDITION_DISPLAY', 'TODAY_VACCINE_CONDITION', 'TODAY_NAT_CONDITION_DISPLAY', 'USER_ID', 'FILL_TIME', 'BY10_DISPLAY', 'DEPT_CODE', 'TODAY_BODY_CONDITION_DISPLAY', 'DEPT_CODE_DISPLAY', 'CHECKED', 'NEED_CHECKIN_DATE', 'CREATED_AT', 'TODAY_SITUATION', 'USER_NAME', 'BY7', 'BY8', 'BY9', 'BY11_DISPLAY']
    now = datetime.now()
    post_info = {}
    for info in raw_info:
        key_value = info.split(':',1)
        key = key_value[0].strip('"')
        val = key_value[1].strip('"')
        if key in post_key:
            if val == 'null':
                post_info[key] = ''
            else:
                post_info[key] = val
    wraw=post_info['USER_ID']+now.strftime("%Y%m%d%H%M%S")
    hl = hashlib.md5()
    wid=hashlib.md5(wraw.encode(encoding='utf-8')).hexdigest()
    post_info['CREATED_AT'] = now.strftime("%Y-%m-%d %H:%M:%S")
    post_info['CZRQ'] = now.strftime("%Y-%m-%d %H:%M:%S")
    post_info['FILL_TIME'] = now.strftime("%Y-%m-%d")+" "+now.strftime("%H:%M:%S")
    post_info['NEED_CHECKIN_DATE'] = now.strftime("%Y-%m-%d")
    post_info['WID'] = wid
    post_info['TODAY_TEMPERATURE'] = str(random.randint(355, 365) / 10).ljust(3, '0')[:4]

    report_url = 'http://i.nuist.edu.cn/qljfwapp/sys/lwNuistHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do'
    report_response = sess.post(report_url, data=post_info, headers=header)
    if report_response.status_code == 200:
        print(f"\033[32m{post_info['USER_ID']}打卡成功！\033[01m")
        title2 = '今日已自动填报'
        content2 = '填报结果\r=========\r\r* **学号**：'+post_info['USER_ID']+'\r\r* **体温**：'+post_info['TODAY_TEMPERATURE']+'\r\r* **日报编号**：'+post_info['WID']+'\r\r* **时间**：'+time.strftime('%Y-%m-%d %H:%M:%S')+'\r\r* **统一认证验证码**：'+captcha+'\r\r填报成功！'
        
    else:
        print(f"\033[31m{post_info['USER_ID']}打卡失败！\033[01m")
        title2 = '今日打卡失败！'
        content2 = '请检查系统状态'

    data2 = {
        "text":title2,
        "desp":content2
        }
    api = f"https://sctapi.ftqq.com/{sct}.send"
    sess.post(api,data = data2)


def main():
    parser = argparse.ArgumentParser(description="NUIST健康日报自动填写")
    parser.add_argument('-m','--mode',help='用户名/密码读取方式。file选项为读取当前目录下user_data.json, manual选项为手动填写。默认为file模式',default='file')
    parser.add_argument('-u','--username',help='一卡通/校园门户用户名，默认为学号')
    parser.add_argument('-p','--password',help='一卡通/校园门户密码')
    parser.add_argument('-b','--bark',help='是否开启Bark推送,默认为F。可选T/F',default='F')
    parser.add_argument('-k','--key',help='Bark推送的个人API',default='')
    parser.add_argument('-t','--title',help='Bark推送标题,默认为"健康日报"。仅在Bark推送开启时奏效',default='健康日报')
    parser.add_argument('-c','--content',help='Bark推送正文。仅在Bark推送开启时奏效')
    parser.add_argument('-s','--server_sct',help='Server酱推送SCT码',default='')
    arg = parser.parse_args()
    mode = arg.mode
    if mode == 'file':
        with open("user_data.json","r") as f:
            user_data = json.load(f)
        username = user_data['username']
        password = user_data['password']
    elif mode == 'manual':
        username = str(arg.username.strip())
        password = str(arg.password.strip())

    if username == None or username == "" or password == None or password == "":
        print(f"\033[31m请正确填写账号密码(当前模式为{mode})\033[01m")
        exit(0)

    sess = requests.session()
    login(sess, username, password)
    report(sess,arg.server_sct)
    sess.close()
    if arg.bark == 'T':
        if arg.key == '':
            print("\033[31mBark的KEY为空\033[01m")
        else:
            url = f'https://api.day.app/{arg.key}/{arg.title}/{arg.content}'
            requests.get(url)
            print("\033[32m完成推送!\033[01m")


if __name__ == '__main__':
    main()
