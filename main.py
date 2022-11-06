import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import re
import time
import pickle



def get_page_weight(up, chat):
    w = chat / up
    if up > 10000:
        return 2
    elif up > 100 and 0.02 < w < 0.5:
        return 1
    else:
        return 0


def get_collection_items(url):
    options = webdriver.ChromeOptions()

    # 不加载图片, 提升速度
    options.add_argument("blink-settings=imagesEnabled=false")

    # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    # options.add_argument("--headless")

    # 以最高权限运行
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    item_limit = int(
        re.findall(
            r"([0-9]+)",
            driver.find_element(
                By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div'
            ).text,
        )[0]
    )
    page_limit = item_limit // 20 + 1
    item_other = item_limit % 20
    if not item_other:
        page_limit -= 1

    collection_pages_list = []

    for pagei in range(1, page_limit + 1):
        if pagei != page_limit or not item_other:
            xx = 21
        else:
            xx = item_other + 1
        for i in range(1, xx):
            # print(pagei)
            try:
                collection_page = driver.find_element(
                    By.XPATH,
                    r'//*[@id="root"]/div/main/div/div[1]/div[2]/div[2]/div[1]/div['
                    + str(i)
                    + r"]/div/div/div",
                )
            
                data1 = collection_page.get_attribute("data-zop")
                data2 = collection_page.get_attribute("data-za-extra-module")
                data1 = json.loads(data1)
                if not data2 or not data1:
                    continue
                data2 = json.loads(data2)
                if data1['type']=='answer':
                    url_head="https://www.zhihu.com/answer/"
                elif data1['type']=='article':
                    url_head='https://zhuanlan.zhihu.com/p/'
                collection_pages_list.append(
                    (   
                        url_head + str(data1["itemId"]),
                        data1["title"],
                        data2["card"]["content"]["upvote_num"],
                        data2["card"]["content"]["comment_num"],
                    ))
            except:
                continue
            
        if pagei == 1:
            x = 7
        elif pagei == page_limit:
            break
        elif pagei <= 3 or pagei >= page_limit - 2:
            x = 8
        else:
            x = 9
        try:
            driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/main/div/div[1]/div[2]/div[2]/div[2]/button['
                + str(x)
                + "]",
            ).click()
            time.sleep(6)
        except:
            driver.quit()
            print(pagei,'程序崩溃')
            return collection_pages_list
    driver.quit()
    return collection_pages_list


def list2set(path,path2):
    with open(path, 'rb') as save_data:
        cl=pickle.load(save_data)

    with open(path2, 'rb') as save_data:
        cll=pickle.load(save_data)
    ccc=[]
    for i in range(3):
        cll[i]+=cl[i]
        ccc.append(list(set(cll[i])))

    with open(path2, 'wb') as save_data:
        pickle.dump(ccc, save_data)

path=r'D:\acode\PYTHON\project\知乎文章抓取\main\ss.pkl'
path2=r'D:\acode\PYTHON\project\知乎文章抓取\main\xx.pkl'
URL = "http://www.zhihu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


with open(path2, 'rb') as save_data:
    cl=pickle.load(save_data)
collection_list_old=cl[2]

pages = {}
main_page = requests.get(URL + "/explore", headers=headers).text
favorite_page = main_page[main_page.find("热门收藏夹") : main_page.find("专栏")]
# answer_items=re.findall(r'href="(http.*?)" target=.*?>(.*?)</a><div.*?CountTag">(.+?) 赞同<.*?>(\d+?) 评论<',favorite_page)
collection_items = re.findall(
    r'ExploreCollectionCard-collectedContentCount" href="(.*?)" target=', favorite_page
)
url_list=[]
title_list=[]
collection_list=[]
time.sleep(3)
try:
    for i in collection_items:
        if i in collection_list_old:
            continue
        print('正在爬取收藏id:'+str(i))
        collection_list.append(i)
        for ii in get_collection_items(URL + i):
            if get_page_weight(ii[2],ii[3]):
                url_list.append(ii[0])
                title_list.append(ii[1])
        
        time.sleep(9)
except:
    print('程序意外终止')
print(url_list)
with open(path, 'wb') as save_data:
    pickle.dump([url_list,title_list,collection_list], save_data) 
    print('已写入')
