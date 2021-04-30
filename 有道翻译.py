import requests
import time
import random
import hashlib

def main():
    word = input("请输入需要翻译的单词：")
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36",
        "Referer": "http://fanyi.youdao.com/",
        "Cookie": "OUTFOX_SEARCH_USER_ID=558911459@10.169.0.84; JSESSIONID=aaacq6L7wcTKvh77zOiFx; OUTFOX_SEARCH_USER_ID_NCOO=1505951417.397322; ___rl__test__cookies=1613978814401",
    }
    timestamp = time.time()*1000
    salt = str(timestamp) + str(random.randint(0,10))
    temp = "fanyideskweb" + word + salt + "Nw(nmmbP%A-r6U3EUn]Aj"
    sign = hashlib.md5(temp.encode("utf-8")).hexdigest()
    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "lts": timestamp,
        "bv": "10ca024c796f59b2c3d4d348f4741a26",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME"
    }
    resp = requests.post(url,headers=headers,data=data)
    print(resp.status_code)
    print(resp.text)
    print(resp.json()["translateResult"][0][0]["tgt"])

if __name__ == '__main__':
    main()