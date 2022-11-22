# 動的に授業データを表示するため不可能
# import requests

import time
# コマンドライン引数を使用
import sys

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

if(login == browser.current_url):
    print("ERROR : ログイン失敗 PW,IDが違います")
    sys.exit()
else:
    print("SUCCESS : 香川大学Moodleへのログイン")

# コース一覧ページ表示
browser.implicitly_wait(3)
browser.get(url)
browser.implicitly_wait(3)

# Depth1

# コース一覧要素を取得
mainElem = browser.find_element(By.ID,"region-main")

# 要素がクリックできない
## コードが機能していないことを疑う
## すべてを展開する をクリック
### 1 クラスで指定
### 2 文字列で指定
### 3 JSで実行（クラスで指定し[0]を選択)
### 4 リンクでアクセス
### A クリック
### B エンターキー送信
#####すべてダメだった
## ボタンを押す場所が悪い？
### 繰り返しボタンを押してやり、成功したらやめる ８〜１０回で行ける
#####いけた ボタンが押される場所はランダムっぽい
### 繰り返しボタン押すの、ダサくない？非効率的じゃない？
### locationで要素の左上隅からの座標を指定できる

# 1
expandBtn = mainElem.find_element(By.CLASS_NAME,"collapseexpand")
# 2
# expandBtn = mainElem.find_element(By.LINK_TEXT,"すべてを展開する")
if expected_conditions.element_to_be_clickable(expandBtn):
    try:
        ## 1A 2A
        # text1 = BeautifulSoup(browser.page_source,"html.parser").find(id="region-main")
        text1 = browser.find_element(By.ID,"region-main").text
        text2 = text1
        n = 0
        while text1 == text2:
            n+=1
            expandBtn.click()
            time.sleep(1)      ## 少しあいだ開け無いと、HTMLがおかしくなる
            text2 = browser.find_element(By.ID,"region-main").text
            ## 1B 2B
            # expandBtn.send_keys(Keys.ENTER)
            ## 3A
            # browser.execute_script("document.getElementsByClassName('collapseexpand')[0].click();")
            ## 4
            # browser.get(expandBtn.get_attribute("href"))
        else:
            print ("SUCCESS : コース一覧で展開ボタンを押す 試行回数%d"% n)
    except:
        print ('ERROR : cannot click "すべてを展開する"')
        sys.exit()
else:
    print('ERROR : cannot click "すべてを展開する" ボタンではありません')
    sys.exit()


# カテゴリーのURLを含むaタグ削除
# ついでに カテゴリー名取れる？
for a in mainElem.find_elements(By.TAG_NAME,"a"):
    removeHref = a.get_attribute("href")
    if type(removeHref) is str:
        print(a.text)
        print("aa")
    try:
        if str(removeHref) in "categoryid":
            print(a.text)
            print("sakujosuru bun kaku")
            print()
    except:
        print("削除失敗")


# notloadedクラスを探し、その中のh4タグをクリックする
notloadedClass = mainElem.find_elements(By.CLASS_NAME, "notloaded")
browser.execute_script("""
    var element = document.querySelector(".notloaded");
    element.parentNode.removeChild(element);
""")
for notloaded in notloadedClass:
    try:
        notloadedh4 = notloaded.find_element(By.TAG_NAME,"h4")
        notloadedh4.click()
        time.sleep(0.5)
    except:
        print("ERROR")


time.sleep(60)
# ブラウザを終了
browser.quit()