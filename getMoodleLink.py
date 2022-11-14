# 動的に授業データを表示するため不可能
# import requests

# コマンドライン引数を使用
import sys

# JSによる動的表示対応
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.chrome import service
# from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
# データ抽出
from bs4 import BeautifulSoup

username = sys.argv[1]
password = sys.argv[2]

login = "https://kadai-moodle.kagawa-u.ac.jp/login/index.php"
url = "https://kadai-moodle.kagawa-u.ac.jp/course/index.php"

# ブラウザーを起動
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
# 暗黙的な待機を最大3秒行う(サーバーの負担軽減)
browser.implicitly_wait(3)

# ログイン
# URLを読み込む
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
browser.get(url)
browser.implicitly_wait(3)

mainElem = browser.find_element(By.ID,"region-main")

# すべてを展開する をクリック
expandBtn = mainElem.find_element(By.CLASS_NAME,"collapseexpand")
if expected_conditions.element_to_be_clickable(expandBtn):
    # print("true")
    try:
        expandBtn.click()
        browser.implicitly_wait(3)
    except:
        print ("ERROR : cannot click")

courseDepth1 = mainElem.find_elements(By.TAG_NAME,"h3")
for a in courseDepth1:
    
    print(a.text)
    if expected_conditions.element_to_be_clickable(a):
        # print("true")
        a.click()
        browser.implicitly_wait(3)

print (browser.find_element(By.ID,"region-main").text)