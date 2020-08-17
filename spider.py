# -*- coding: utf-8 -*-
# @Time    : 2020-8-13 14:54
# @Author  : lzh
# @Email   : 1096495142@qq.com
# @File    : spider.py
# @Software: PyCharm

from bs4 import BeautifulSoup #网页解析，获取数据
import re  #正则表达式，进行文字匹配
import urllib.request,urllib.error #制定url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行SQLite操作

def main():
    baseUrl = "https://movie.douban.com/top250?start="
    savePath = '豆瓣电影top250.xls'
    dbpath = 'movietop250.db'
    #1.获取数据
    dataList = getData(baseUrl)
    #3.保存数据excel
    # saveData(dataList,savePath)
    # 3.保存数据到数据库
    saveDataDB(dataList,dbpath)
    print('爬取完毕')

#影片详情链接的正则
findLink = re.compile(r'<a href="(.*?)">') #创建正则表达式对象
#影片图片链接的正则
findImageSrc = re.compile(r'<img.*src="(.*?)".*>',re.S) #re.S 让换行符包含在字符中
#影片名
findTitle = re.compile(r'<span class="title">(.*?)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findIng = re.compile(r'<span class="inq">(.*?)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#1.获取数据
def getData(baseUrl):
    index = 0
    dataList = []
    for i in range(0,10):#调用获取页面函数，10次
        url = baseUrl + str(i*25)
        html = askUrl(url)
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"): #查找符合要求的字符串形成列表
            data = []
            item = str(item)
            #影片详情的连接
            link = re.findall(findLink,item)[0] #re库用来通过正则表达式查找指定字符串
            data.append(link)
            #影片图片链接
            imgSrc = re.findall(findImageSrc,item)[0]
            data.append(imgSrc)
            #影片标题
            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace('/','  ')
                data.append(otitle)
            else:
                ctitle = titles[0]
                data.append(ctitle)
                data.append("  ")
            #影片评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            #找到评价人数
            judge = re.findall(findJudge,item)[0]
            data.append(judge)
            # 找到概况
            ing = re.findall(findIng,item)
            if len(re.findall(findIng,item))>0:
                ing = ing[0].replace('。',"  ")
                data.append(ing.strip())
            else:
                data.append("  ")
            #找到影片的相关内容
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br/>',' ',bd)
            bd = re.sub('/',' ',bd)
            data.append(bd.strip())
            dataList.append(data)
    return dataList

# 得到指定url的网页内容
def askUrl(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
    }
    requset = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(requset)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#3.保存数据到excel
def saveData(datalist,savePath):
    # 2.逐一解析数据
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)
    col = ('电影详情链接','图片链接','影片中文名','外国名','评分','评价数','概况','相关信息')
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print('第%d条数据'%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savePath)

#3.保存数据到数据库
def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:#数字不用加"
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into movie250 (info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values(%s)
        '''%",".join(data)
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print('保存数据到数据库完成')

# 初始化数据库
def init_db(dbpath):
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print('数据库创建成功')

if __name__ == "__main__":#当程序执行时
    # init_db('test.db')
    main()