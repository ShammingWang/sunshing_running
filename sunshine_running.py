"""

a python script for sunshine running
you just need the IMEI (such as ceafd177af5047cf848a6f1d3d2e61fd)
by Shamming

$ pip install requests

"""
import requests
import json
import random


def encrypt(s):
    ans = ''
    for i in s:
        ans += table[ord(i) - ord('0')]
    return ans


# 随机取十个字母放入table
alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)
table = ''.join(alphabet)[0:10]

root = 'http://client3.aipao.me/api/'
# IMEICode = 'ceafd177af5047cf848a6f1d3d2e61fed'
IMEICode = input('请输入IMEI:')
start_url = root + 'token/QM_Users/LoginSchool?IMEICode=' + IMEICode
Session = requests.session()
# 利用IMEI获取token信息 但是IMEI 每周刷新
start_res = Session.get(url=start_url)
start_res.encoding = start_res.apparent_encoding
# 将网页返回的json类型的数据转化成python的字典
start_data = json.loads(start_res.content.decode('utf-8'))['Data']
Token_val = start_data['Token']
# print('获取到的Token值为：', Token_val)
identity_url = root + Token_val + '/QM_Users/GS'
identity_res = Session.get(url=identity_url)
identity_res.encoding = identity_res.apparent_encoding
print(identity_res.text)
identity_data = json.loads(identity_res.content.decode('utf-8'))['Data']
User = identity_data['User']
SchoolRun = identity_data['SchoolRun']

run_url = root + Token_val + '/QM_Runs/SRS?S1=30.534736&S2=114.367788&S3=' + str(SchoolRun['Lengths'])
# print(run_url)
run_res = Session.get(url=run_url)
# print(run_res.text)
run_data = json.loads(run_res.content.decode('utf-8'))['Data']
StartTime = run_data['StartTime']
RunId = run_data['RunId']
run_time = str(random.randint(720, 900))  # seconds
run_dist = str(SchoolRun['Lengths'] + random.randint(0, 3))  # meters
run_step = str(random.randint(1300, 1800))  # steps

end_url = root + '/' + Token_val + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
          encrypt(run_time) + '&S5=' + encrypt(run_dist) + \
          '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(run_step)
end_res = Session.get(url=end_url)
print(end_res.text)
end_data = json.loads(end_res.content.decode('utf-8'))['Data']

if json.loads(end_res.content.decode('utf-8'))['Success']:
    print(StartTime)
    print('------------跑步成功------------')
    print('跑步时间:', int(run_time) // 60, '分', int(run_time) % 60, '秒')
    print('跑步距离:', int(run_dist), '米')
    print('跑步步数:', int(run_step))
    print('------------跑步结束------------')
else:
    print('------------跑步失败------------')
