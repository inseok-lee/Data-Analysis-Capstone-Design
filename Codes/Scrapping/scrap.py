import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# '사랑' 키워드 검색 후 첫 페이지(URL)
URL_Base = 'https://www.melon.com'
#두려움
#URL_Sub = '/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=두려움'
#걱정
URL_Sub = '/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=걱정'
#불안
#URL_Sub = '/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=걱정'
#우울
#URL_Sub = '/dj/djfinder/djfinder_inform.htm?djSearchType=T&djSearchKeyword=걱정'

URL = URL_Base + URL_Sub

# 크롬 드라이버 추가
driver = webdriver.Chrome(executable_path='chromedriver_mac64_m1')
driver.get(url=URL)

songs = []  # 곡 제목
lyrics = []  # 가사
error_count = 0

# 각 DJ의 xpath 추가(한 페이지 내의 DJ)
dj_xpath = []
for n in range(20):
    #//*[@id="djPlylstList"]/div/ul/li[1]/div[2]/div[1]/a[2]
    #//*[@id="djPlylstList"]/div/ul/li[2]/div[2]/div[1]/a[2]
    xpath = "//*[@id=\"djPlylstList\"]/div/ul/li[{}]/div[2]/div[1]/a[2]".format(n + 1)
    dj_xpath.append(xpath)

# DJ 루프

for i in range(len(dj_xpath)):
    driver.get(url=URL)
    # 페이지 이동
    # page = driver.find_element_by_xpath('//*[@id="pageObjNavgation"]/div/span/a[2]')
    # page.click()
    # time.sleep(0.3)

    # DJ 페이지로 이동
    dj_page = driver.find_element_by_xpath(dj_xpath[i])
    dj_page.click()
    time.sleep(0.3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # DJ 수록곡 수 확인
    raw = soup.find("span", {"class": "sum"})
    count_songs = int(raw.text[1:-1])  # 숫자만 뽑아내기
    q = count_songs // 50  # 총 페이지 수 확인
    r = count_songs % 50  # 마지막 페이지 곡 수
    # print(count_songs)
    # print(q, r)

    if q > 4:
        break

    # 페이지 루프(50 곡이 넘어갈경우)
    for j in range(q + 1):
        song_list = driver.find_elements(By.CSS_SELECTOR, ".btn.button_icons.type03.song_info")
        print(len(song_list))

        # 곡 루프
        for k in range(0, len(song_list)):
            song_list = driver.find_elements(By.CSS_SELECTOR, ".btn.button_icons.type03.song_info")
            song_list[k].click()
            time.sleep(0.3)

            try:
                t = driver.find_element(By.CSS_SELECTOR, ".song_name")
                songs.append(t.text)
                time.sleep(0.1)

                driver.find_element(By.CSS_SELECTOR, '.button_more.arrow_d').click()
                l = driver.find_element(By.CSS_SELECTOR, ".lyric.on")
                lyrics.append(l.text)
                time.sleep(0.1)

            except:
                error_count += 1
                print("에러 발생 수 : {}".format(error_count))
                print("인덱스 : {}".format(i))
                driver.back()
                continue

            driver.back()

        # DJ 플레이리스트의 마지막 페이지인 경우
        if j == q:
            break

        # 50곡 단위로 페이지 넘기기
        page_xpath = "//*[@id=\"pageObjNavgation\"]/div/span/a[{}]".format(j + 1)
        next_page = driver.find_element_by_xpath(page_xpath)
        next_page.click()
        time.sleep(0.3)

driver.close()

result= {"제목": songs , "가사": lyrics}
df = pd.DataFrame(result)  #df로 변환

# csv 파일로 저장
df.to_csv('song_worry.csv')