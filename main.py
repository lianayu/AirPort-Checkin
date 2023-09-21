import requests
import json
import os
import time
import random

# ql脚本 增加环境变量：AIRPORT_ACCOUNT（多账号格式：账号|密码;账号|密码） AIRPORT_BASE_URL
# session.get(base_url,headers=headers, verify=False) 不加header 运行不了 

requests.packages.urllib3.disable_warnings()

def multi_account():
    accounts = os.environ["AIRPORT_ACCOUNT"]# 账号|密码;账号|密码
    account = accounts.split(';')
    for i in range(len(account)):
        st=random.randint(2,30)
        print("sleep ",st)
        time.sleep(st)
        u_p = account[i].split("|")
        email = u_p[0]
        password = u_p[1]
        checkin(email,password)
        
def checkin(email, password, base_url=os.environ['AIRPORT_BASE_URL'], ):
    #email = email.split('@')
    #email = email[0] + '%40' + email[1]

    session = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    session.get(base_url,headers=headers, verify=False)
    login_url = base_url + '/auth/login'
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    
    response = session.post(login_url, post_data, headers=headers, verify=False)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': base_url + '/user'
    }
    
    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
    response.encoding='utf-8' #感觉没啥用
    print(email,response.status_code,response.text)
    return response.status_code

result = multi_account()
