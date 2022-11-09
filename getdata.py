#2つのライブラリをインストール（今回はこっちを使う）
#Requests をインストール Webページを取得する
#Beautiful Soupをインストール（データ抽出用）インストールが嫌ならHTMLPerserっていうのが標準で使えるらしい

#こっちだと１つのみのインストールで良い
#JavaScriptが使用されている場合はSeleniumがよく利用される 

# 取得日時取得
import time
# エラーハンドリング
import traceback

# Webページ取得（動的表示には非対応のためお役御免）
# import requests

# JSによる動的表示対応
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
import chromedriver_binary
# データ抽出
from bs4 import BeautifulSoup

url = "https://www2.st.kagawa-u.ac.jp/Portal/Public/Syllabus/SearchMain.aspx"
year = "2022"
faculties = "00"

# ブラウザーを起動
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
# 暗黙的な待機を最大3秒行う(サーバーの負担軽減)
browser.implicitly_wait(3)
# URLを読み込む
browser.get(url)
# htmlを取得

# 年の要素を見つける
yearElement = browser.find_element(By.NAME,"ctl00$phContents$ddl_year")
# 要素を選択
yearSelect = Select(yearElement)
# 値を入力
yearSelect.select_by_value(year)

# 開講学部の要素を見つける
facultiesElement = browser.find_element(By.NAME,"ctl00$phContents$ddl_fac")
# 要素を選択
facultiesSelect = Select(facultiesElement)
# 値を入力
facultiesSelect.select_by_value(faculties)

#検索ボタンを見つける
searchBtnElement = browser.find_element(By.NAME,"ctl00$phContents$btnSearch")
# クリック
searchBtnElement.click()

html = browser.page_source

soup = BeautifulSoup( html, 'html.parser')
#  時間割データがあるtableを抜き取り
# soup = soup.find(By.ID,"ctl00_phContents_ucGrid_grv")
soup = soup.find("table")
# table = soup[0]

# 各行ごと
f = open("test.csv", "w")

for tableLine in soup.find_all("tr"):
    # print(tableLine)
    for tableCell in tableLine.find_all("td"):
        print("%s, "% tableCell.text,file=f)
    # print ("\n" ,file=f)

f.close()
# ブラウザを終了
browser.quit()
