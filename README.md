# Wallpaper crawling
import requests,json
import re
from bs4 import BeautifulSoup
import time
def pa(sum,sum2):
    lianjie = []
    def pachong(url):
        res = requests.get(url)
        print('状态：'+str(res.status_code))
        bs = BeautifulSoup(res.text,'html.parser')
        li = []
        for i in bs.find_all('img'):
            li.append(i['src'])
        #获取壁纸链接----------------------

        
        for y in li:
            #name = re.findall(r'thumbs/(.*)',y)#提取链接名称作为文件名
            name1 = re.findall(r'thumbs/(.*)-t1',y)#提取名称拼接成下载链接
            lianjie.append(f'http://wallpaperswide.com/download/{name1[0]}-1920x1080.html')#拼接下载链接
            #print(f'当前爬取链接：{lianjie}')
            #res_1 = requests.get(lianjie)
            #op = open('C:\\壁纸\\001.txt','a')
            #op.write(res_1.content)
            #op.close()
    

        # for tp in range(3918):
        # url = f'http://wallpaperswide.com/page/{tp}'
        # pachong(url)
        # time.sleep(1)
        # print('开始爬取：'+url)
    for i in range(sum,sum2):
        url = f'http://wallpaperswide.com/page/{i}'
        pachong(url)
        print(f'开始爬取：{url}')
        time.sleep(1)



    op = open('C:\\003.txt','w')
    op.write(json.dumps(lianjie))
    op.close()
    return '成功'

pa(50,100)
