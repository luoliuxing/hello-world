from gevent import monkey

monkey.patch_all()
from gevent.queue import Queue
import gevent, requests, openpyxl, json
from lxml import etree
import os, copy

welcome = '''

       ------------------------------------------------------                                                  
        全国消毒产品网上备案信息服务平台消毒产品备案信息查询    
       ------------------------------------------------------                                                   

'''

print(welcome)
os.makedirs('data', exist_ok=True)  # 生成目录
list_shibai = []  # 初始化失败列表
work_1 = Queue(100)  # 创建queue对象
work = Queue()  # 创建queue对象
t = 0


# 创建表格的函数
def chuangjiangbiaoge(name):
    # table = name
    book = openpyxl.Workbook()
    sh = book.active
    sh.title = 'tab1'

    # 写标题栏
    sh['A1'] = 'ID'
    sh['B1'] = '产品名称'
    sh['C1'] = '产品分类'
    sh['D1'] = '评价日期'
    sh['E1'] = '产品责任单位名称'
    sh['F1'] = '检验报告结论'
    sh['G1'] = '卫生安全评价结论'
    sh['H1'] = '备案日期'
    sh['I1'] = '生产企业名称'
    sh['J1'] = '生产企业卫生许可证号'
    sh['K1'] = '剂型'
    sh['L1'] = '型号'
    sh['M1'] = '产品使用范围'
    sh['N1'] = '检测机构1'
    sh['O1'] = '检测机构2'
    sh['P1'] = '检测机构3'
    sh['Q1'] = '检测机构4'
    sh['R1'] = '检测机构5'
    sh['S1'] = '检测机构6'
    sh['T1'] = '检测机构7'
    sh['U1'] = '检测机构8'
    sh['V1'] = '检测机构9'
    sh['W1'] = '检测机构10'
    sh['X1'] = '检测机构11'
    sh['Y1'] = '检测机构12'
    sh['Z1'] = '检测机构13'
    book.save(f'data\\{name}.xlsx')


# 获取id的函数
def dower_id(name):
    try:
        url = 'https://credit.jdzx.net.cn/xdcp/elasticsch/showByName.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        data = {
            'productSearch': name
        }
        response = requests.post(url=url, headers=headers, data=data)

        js = response.json()
        txt = json.loads(js['data'])
        lin = []
        for i in txt:
            lin.append(i['id'])
        return lin
    except Exception as e:
        print(f'未知异常:', e)


# 下载数据函数
def dower_wenjian():
    global t
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    while not work.empty():
        i = work.get_nowait()  # 从队列里取数据
        print(f'正在执行：{i}', f'剩余：{work.qsize()}')

        # 写入表格的列表
        list_com = []
        list_com.append(i)
        url = f'https://credit.jdzx.net.cn/xdcp/productSearch/product_nologin?ID={i}&flag={i}&a='
        try:
            response = requests.get(url=url, headers=headers)
            tree = etree.HTML(response.text)

            basic = tree.xpath(
                '//div[@id="pageForm"]/div[@id="showOne"]/div[@class="basic"]/table[@class="showPage"]//tr[@class="tr-odd"]')
            list_com.append("".join(basic[1].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[2].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[3].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[4].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[7].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[8].xpath('.//span//text()')[1:]))
            list_com.append("".join(basic[9].xpath('.//span//text()')[1:]))

            showMakeComp0 = tree.xpath(
                '//div[@id="pageForm"]/div[@id="showOne"]/table[@id="showMakeComp0"]//tr[@name="desy"]')[1:]
            list_p = []
            list_p2 = []
            for o in showMakeComp0:
                p = o.xpath('.//span//text()')
                try:
                    list_p.append(p[0])
                    list_p2.append(p[1])
                except:
                    list_p.append('无')
                    list_p2.append('无')
            list_com.append("   ".join(list_p))
            list_com.append("   ".join(list_p2))

            showdash = tree.xpath(
                '//div[@id="pageForm"]/div[@id="showOne"]/table[@id="showdash"]//td[@class="td-other"]')
            list_com.append("".join(showdash[0].xpath(".//span//text()")[1:]))
            list_com.append("".join(showdash[1].xpath(".//span//text()")[1:]))
            list_com.append("".join(showdash[2].xpath(".//span//text()")[1:]))

            lis = []
            showreportlist = tree.xpath(
                '//div[@id="pageForm"]/div[@id="showOne"]/table[@id="showReportList"]//tr[@name="desy"]')[1:]
            for show in showreportlist:
                n = show.xpath('.//span//text()')
                lis.append(n[0])
            for li in list(set(lis)):
                list_com.append(li)

            work_1.put(list_com, timeout=60)  # 存数据进队列
        except Exception as e:
            print(f'未知异常:{i}', e)
            list_shibai.append(i)
            t += 1



def baochun_table(tab_name, ksum):
    global t
    # 加载 excel 文件
    wb = openpyxl.load_workbook(f'data\\{tab_name}.xlsx')
    # 得到sheet对象
    sheet = wb['tab1']
    s = 0
    while not ksum == s+t:
        try:
            i = work_1.get(timeout=2)
        except:
            print('等待超时，继续等待')
        else:
            sheet.append(i)
            s += 1
    print(f'队列总数：{ksum},成功{s},失败{t}')
    wb.save(f'data\\{tab_name}.xlsx')


def xiecheng(listt, tab_name):
    for url in listt:
        work.put_nowait(url)  # 存数据进队列

    listt.clear()
    ksum = work.qsize()
    tasks_list = []
    for x in range(50):
        tasks_list.append(gevent.spawn(dower_wenjian))
    tasks_list.append(gevent.spawn(baochun_table, tab_name, ksum))
    print('开始任务~')
    gevent.joinall(tasks_list)


def dysb(name):
    global t
    for i in range(1, 4):
        if not len(list_shibai) == 0:
            print('开始失败重试', i)
            new_list = copy.deepcopy(list_shibai)
            list_shibai.clear()
            t = 0
            xiecheng(new_list, name)
        else:
            break
    print(f'任务结束总共：{len(list_shibai)}失败,已保存到本地')  # 统计失败条数
    # 失败id保存为txt文本
    if not len(list_shibai) == 0:
        fn = open(f'data\\{name}.txt', 'w', encoding='utf-8')
        fn.write(json.dumps(list_shibai))
        fn.close()
        list_shibai.clear()
        t = 0
    else:
        if os.path.exists(f'data\\{name}.txt'):
            os.remove(f'data\\{name}.txt')


while True:
    nn = input('请选择功能：1、新建下载 2、继续下载 3、退出：')
    if nn == '1':
        name = input('请输入要查询的关键字：')
        if os.path.exists(f'data\\{name}.xlsx'):
            print(f'{name}.xlsx文件已存在，请删除再重新下载')
            continue
        try:
            lin = dower_id(name)
            one = input(f'总共：{len(lin)}条数据,输入Y下载，任意字符取消：')
            if one == 'Y':
                chuangjiangbiaoge(name)  # 创建表格
                xiecheng(lin, name)  # 开启协程
                dysb(name)
        except Exception as e:
            print('未知异常:', e)
    elif nn == '2':
        name_1 = input('请输入关键字：')
        try:
            op = open(f'data\\{name_1}.txt', 'r', encoding='utf-8')
            liebiao = json.loads(op.read())
            op.close()
            xiecheng(liebiao, name_1)
            dysb(name_1)
        except Exception as e:
            print('未知异常:', e)
    elif nn == '3':
        break
    else:
        print('输入有误~')
