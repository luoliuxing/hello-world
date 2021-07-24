from gevent import monkey
monkey.patch_all()
# monkey.patch_all()能把程序变成协作式运行，就是可以帮助程序实现异步。
from gevent.queue import Queue  # 从gevent库里导入queue模块
import os
import gevent
import re
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/66.0.3329.0 Mobile Safari/537.36'
}


def get_uid():  # 输入链接获取用户id
    global headers
    while True:
        url = input('请输入链接：')  # 分享的链接
        if not url.startswith('https'):
            print('链接有误！')
        elif url.find('douyin.com') == -1:
            print('不是抖音链接~')
        else:
            try:
                response = requests.get(url, headers=headers)
                redirect_url = response.url
                sec_uid = re.match(r".*sec_uid=(.*?)&", redirect_url).group(1)
                print(sec_uid)
                return sec_uid
            except Exception as e:
                print('未知异常：', e)


# 爬取用户数据函数
def nex(max_1, us):
    global headers
    params = {
        'sec_uid': us,
        'count': '21',
        'max_cursor': max_1,
        'aid': '1128',
        '_signature': '3AkC6QAAvHA7fvrvDif6nNwJAv',
    }
    url = "https://www.iesdouyin.com/web/api/v2/aweme/post/"
    print(f'正在爬取:{max_1}')
    result = requests.get(url, headers=headers, params=params)  # 爬取数据
    json_str = result.json()  # 将返回的json数据转换为字典对象
    max_cursor = json_str['max_cursor']
    aweme_list = json_str['aweme_list']
    return max_cursor, aweme_list


def paqusuoyoulianjie():  # 生成链接列表
    maxq = '0'
    lit = []
    usid = get_uid()
    while True:
        max_cursor, aweme_list = nex(maxq, usid)
        if not aweme_list:
            print('爬取完成！！')
            return lit
        else:
            for i in aweme_list:
                try:
                    url_1 = i['video']['play_addr']['url_list'][0]
                    name = i['aweme_id']
                    title = i['desc']
                    nickname = i['author']['nickname']
                    a = {'name': name, 'title': title, 'url_1': url_1, 'nickname': nickname}
                    lit.append(a)
                except Exception as e:
                    print('未知异常:', e)
            maxq = max_cursor


def get_douying():  # 批量下载视频
    translist = paqusuoyoulianjie()  # 获取全部连接
    niu_id = translist[0]['nickname']
    os.makedirs(niu_id, exist_ok=True)  # 生成目录

    work = Queue()  # 创建队列对象
    tasks_list = []
    # 创建空的任务列表

    for i in translist:
        work.put_nowait(i)  # 添加数据进队列

    def crawler():
        while not work.empty():  # 判断队列是否为空
            data = work.get_nowait()  # 从队列取数据
            print(f'队列剩余数据：{work.qsize()}')
            url = data['url_1']
            name = data['title'] + data['name']
            repost = requests.get(url)
            fis = f'''{niu_id}\\{name}.mp4'''
            w = open(fis, 'wb')
            w.write(repost.content)
            w.close()

    for x in range(20):
        # 创建爬虫
        task = gevent.spawn(crawler)
        # 用gevent.spawn()函数创建执行crawler()函数的任务。
        tasks_list.append(task)
        # 往任务列表添加任务。

    gevent.joinall(tasks_list)  # 用gevent.joinall方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站。


if __name__ == '__main__':
    get_douying()
