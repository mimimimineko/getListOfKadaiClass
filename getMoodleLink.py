# 動的に授業データを表示するため不可能
# import requests

import time
# コマンドライン引数を使用
import sys

# 木構造
from anytree import Node, RenderTree

# 多次元配列（リスト）用
import numpy as np

# JSによる動的表示対応
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.chrome import service
from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
# データ抽出
from bs4 import BeautifulSoup




# カテゴリー数を返す
def getList(mainElem,parent):
    num = 0
    h3elem = mainElem.find_elements(By.TAG_NAME,"h3")
    # print("C",end=" ")
    # print(len(h3elem))
    if len(h3elem) != 0:
        for h3 in h3elem:
            h3 = h3.find_element(By.TAG_NAME,"a")
            # 授業名、カテゴリー名
            name = h3.text
            # print("SET: "+name,end=",")
            # URL
            href =h3.get_attribute("href")
            # print(href)
            # 木構造リストに格納
            i = 0
            if "categoryid" not in href:
                i =1
                num +=1
            exec("name = Node((name,href,i),parent=parent)")
    else:
        aelem = mainElem.find_elements(By.CLASS_NAME,"coursename")
        for a in aelem:
            a = a.find_element(By.TAG_NAME,"a")
            name = a.text
            # print("SET: "+name,end=",")
            href = a.get_attribute("href")
            # print(href)
            exec("name = Node((name,href,1),parent=parent)")
    return num


if(len(sys.argv)!=3):
    print("ERROR : $ ファイル名 香大ID PW  のように入力し実行してください。")
    print("通信はこのPCのChromeを用い、httpsでセキュアに行われます")
    sys.exit()
else:
    print("SUCCESS : 引数の数チェック")

username = sys.argv[1]
password = sys.argv[2]

login = "https://kadai-moodle.kagawa-u.ac.jp/login/index.php"
url = "https://kadai-moodle.kagawa-u.ac.jp/course/index.php?categoryid=185"

f = open("test2.csv", "w") # 保存先

# ブラウザーを起動
options = Options()
# options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
# 暗黙的な待機を最大3秒行う(サーバーの負担軽減)
browser.implicitly_wait(3)

# ログイン
browser.get(login)
loginUsernameElem = browser.find_element(By.ID,"username")
loginUsernameElem.clear()
loginUsernameElem.send_keys(username)
loginPasswordElem = browser.find_element(By.ID,"password")
loginPasswordElem.clear()
loginPasswordElem.send_keys(password)
loginBtnElem = browser.find_element(By.ID,"loginbtn")
loginBtnElem.click()
browser.implicitly_wait(3)

if(login == browser.current_url):
    print("ERROR : ログイン失敗 PW,IDが違います")
    sys.exit()
else:
    print("SUCCESS : 香川大学Moodleへのログイン")

# コース一覧ページ表示
browser.get(url)
browser.implicitly_wait(3)

# Depth1

# コース一覧要素を取得
# (授業名、URL、カテゴリーだったら0 コースだったら1)
urlList = Node(("root",url,0),parent=None)
parent = urlList

mainElem = browser.find_element(By.CLASS_NAME,"course_category_tree")
# h3tags = mainElem.find_elements(By.TAG_NAME,"h3")

getList(mainElem,parent)

for a in RenderTree(parent).node.children:
    if "category" in a.name[1]:
        categoryUrl=a.name[1]+"&perpage=200"
        print("GET: "+a.name[0])
        browser.get(categoryUrl)
        browser.implicitly_wait(3)
        parent = a
        try:
            mainElem = browser.find_element(By.CLASS_NAME,"course_category_tree")
            h3tags = mainElem.find_elements(By.TAG_NAME,"h3")
            getList(mainElem,parent)

            for a in RenderTree(parent).node.children:
                if "category" in a.name[1]:
                    categoryUrl=a.name[1]+"&perpage=200"
                    # print("  GET: "+a.name[0])
                    browser.get(categoryUrl)
                    browser.implicitly_wait(3)
                    parent = a
                    try:
                        mainElem = browser.find_element(By.CLASS_NAME,"course_category_tree")
                        h3tags = mainElem.find_elements(By.TAG_NAME,"h3")

                        getList(mainElem,parent)

                        for a in RenderTree(parent).node.children:
                            if "category" in a.name[1]:
                                categoryUrl=a.name[1]+"&perpage=200"
                                # print("    GET: "+a.name[0])
                                browser.get(categoryUrl)
                                browser.implicitly_wait(3)
                                parent = a
                                try:
                                    mainElem = browser.find_element(By.CLASS_NAME,"course_category_tree")
                                    h3tags = mainElem.find_elements(By.TAG_NAME,"h3")
                                    getList(mainElem,parent)
                                except:
                                    continue
                    except:
                        continue
        except:
            continue

for pre, fill, node in RenderTree(urlList):
    print("%s%s%s" % (pre, node.name,node.depth))
    print("%s%s" % (node.depth,node.name),file=f)







# 「すべてを展開する」をクリック
# expandBtn = mainElem.find_element(By.CLASS_NAME,"collapseexpand")
# if expected_conditions.element_to_be_clickable(expandBtn):
#     try:
#         text1 = browser.find_element(By.CLASS_NAME,"course_category_tree").text
#         text2 = text1
#         n = 0
#         while text1 == text2:
#             n+=1
#             expandBtn.click()
#             time.sleep(1)      ## 少しあいだ開け無いと、HTMLがおかしくなる
#             text2 = browser.find_element(By.ID,"region-main").text
#             ## 1B 2B
#             # expandBtn.send_keys(Keys.ENTER)
#             ## 3A
#             # browser.execute_script("document.getElementsByClassName('collapseexpand')[0].click();")
#             ## 4
#             # browser.get(expandBtn.get_attribute("href"))
#         else:
#             print ("SUCCESS : コース一覧で展開ボタンを押す 試行回数%d"% n)
#     except:
#         print ('ERROR : cannot click "すべてを展開する"')
#         sys.exit()
# else:
#     print('ERROR : cannot click "すべてを展開する" ボタンではありません')
#     sys.exit()







# for a in mainElem.find_elements(By.TAG_NAME,"a"):
#     removeHref = a.get_attribute("href")
#     print(removeHref)
#     if type(removeHref) is str:
#         try:
#             if "categoryid" in str(removeHref):
#                 print(a.text)
#                 print("sakujosuru bun kaku")
#                 print()
#         except:
#             print("削除失敗")
# time.sleep(60)

# # notloadedクラスを探し、その中のh4タグをクリックする
# notloadedClass = mainElem.find_elements(By.CLASS_NAME, "notloaded")

# for notloaded in notloadedClass:
#     try:
#         notloadedh4 = notloaded.find_element(By.TAG_NAME,"h4")
#         notloadedh4.click()
#         time.sleep(0.5)
#     except:
#         print("ERROR")


# time.sleep(6000)
# ブラウザを終了
browser.quit()