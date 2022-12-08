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
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
# データ抽出
from bs4 import BeautifulSoup


def getdataByFaculties(faculties):
    # URLを読み込む
    browser.get(url)

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


    # 表示件数設定の要素を見つける
    browser.implicitly_wait(3)
    displayNumElement = browser.find_element(By.NAME,"ctl00$phContents$ucGrid$ddlLines")
    # 要素を選択
    displayNumSelect = Select(displayNumElement)
    # 値を入力
    displayNumSelect.select_by_value("0")
    browser.implicitly_wait(3)



    html = browser.page_source

    soup = BeautifulSoup( html, 'html.parser')

    soup = soup.find("table") #  時間割データがあるtableを抜き取り


    page="1"  #ページ数カウント
    num = "1" #行数カウント
    # 検索結果1ページ分
    # 1行分
    for tableLine in soup.find_all("tr"):
        m = 0 # 列カウント
        fileok = 0

        for tableCell in tableLine.find_all("td"):
            # 授業内容を取る
            if m == 0:  # 検索結果 1列目
                if tableCell.text == str(num) : # 1列目のセルと記録する行番号が同じ時
                    print('"%s, "'% tableCell.text,file=f,end="")
                    fileok = 1 # この行はファイル書き込みしてOK
                    num = int(num) +1
                    m+=1
                else:
                    break #不適合な行はさようなら
            else: # 1列目以外は（不適合なものは弾いたあと）
                print('"%s", '% tableCell.text,file=f,end="")
                m+=1   
        if fileok == 1: # ファイルに書き込んだ行の出力が終わったら 改行
            print ("" ,file=f)

        # 全件表示できることに気づかなかったときに書いたコード
        # if int(num)!=1 and int(num) % 100 == 1: #検索結果最後の行を記録し終えた時(次の行が101,201,301行目の時)
        #     for nextPageCell in tableLine.find_all("a"):
        #         # print (nextPageCell.text)
        #         if nextPageCell.text == str( int(page) + 1 ): #次のページへのリンクがあれば
        #             print("Yes")
        #             nextPageCell.send_keys(Keys.ENTER) #クリック
        #             # nextPageCell.click() #クリック
        #             browser.implicitly_wait(3)
        #             html = browser.page_source
        #             print (html)




f = open("syllabus.csv", "w",encoding="cp932") # 保存先
url = "https://www2.st.kagawa-u.ac.jp/Portal/Public/Syllabus/SearchMain.aspx"
year = "2022"
faculties = "00"

# ブラウザーを起動
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)

getdataByFaculties(faculties)

f.close()
# ブラウザを終了
browser.quit()