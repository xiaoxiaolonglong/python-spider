# -*- coding: utf-8 -*-
# @Time    : 2020-8-13 15:10
# @Author  : lzh
# @Email   : 1096495142@qq.com
# @File    : testUrllib.py
# @Software: PyCharm

import urllib.request

#获取一个get请求
# response = urllib.request.urlopen("http://www.baidu.com")
# print (response.read().decode("utf-8"))

#获取一个post请求
# import urllib.parse
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response = urllib.request.urlopen("http://httpbin.org/post",data=data)
# print (response.read().decode("utf-8"))

#超时处理
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.1)
#     print (response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("time out")

#设置headers
url = "https://www.douban.com"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
}
req = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))