import time
from selenium import webdriver
import pandas as pd

# 멜론차트(URL)
URL = 'https://www.melon.com/chart/index.htm'

# 크롬 드라이버 추가
driver = webdriver.Chrome('chromedriver_win32.exe')
#driver.maximize_window() # 크롬창 크기 최대
driver.get(URL)

# 리스트 초기화
songs = [] # 곡 제목
lyrics = [] # 가사
error_count = 0


# 차트파인더 클릭
chart_finder = driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span')
chart_finder.click()
time.sleep(0.3)

# 연도차트 클릭
year_chart = driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[3]/a')
year_chart.click()
time.sleep(0.1)

for i in range(4): # 연대 루프
    # if i != 0:
    #     # 차트파인더 클릭
    #     chart_finder = driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span')
    #     chart_finder.click()
    #     time.sleep(0.2)
    #
    #     # 연도차트 클릭
    #     year_chart = driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[3]/a')
    #     year_chart.click()
    #     time.sleep(0.1)

    # 연대선택->0000 클릭
    era_xpath = '//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[{}]/span/label'.format(i+1)
    era = driver.find_element_by_xpath(era_xpath)
    era.click()
    time.sleep(0.1)

    for j in range(10): # 연도 루프
        if i == 0 and j == 2: # 2021, 2020 년도 예외처리
            break

        # 연도선택->0000 클릭
        year_xpath = '//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[{}]/span/label'.format(j+1)
        year = driver.find_element_by_xpath(year_xpath)
        year.click()
        time.sleep(0.1)

        # 장르/스타일->국내종합 클릭
        genre = driver.find_element_by_xpath(
            '//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[2]/span/label')
        genre.click()
        time.sleep(0.1)

        # 검색버튼 클릭
        search = driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span')
        search.click()
        time.sleep(0.1)

        for m in range(2): # 1-50 / 51-100
            if m == 0: # 1-50
                song_list = driver.find_elements_by_xpath('//*[@id="lst50"]/td[4]/div/a/span')
            else: # 51-100
                song_list = driver.find_elements_by_xpath('//*[@id="lst100"]/td[4]/div/a/span')

            for n in range(len(song_list)):
                song_list[n].click()
                time.sleep(0.3)

                try:
                    t = driver.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[1]')
                    songs.append(t.text) # 제목 추가
                    driver.find_element_by_xpath('//*[@id="lyricArea"]/button').click()
                    time.sleep(0.1)
                    l = driver.find_element_by_xpath('//*[@id="d_video_summary"]')
                    lyrics.append(l.text) # 가사 추가

                except:
                    error_count += 1
                    print("에러 발생 수 : {}".format(error_count))
                    print("인덱스 : {}".format(n))
                    driver.back()
                    continue

                driver.back()

            # 51-100위
            second_page = driver.find_element_by_xpath('//*[@id="frm"]/div[2]/span/a')
            second_page.click()
            time.sleep(0.3)

print(len(songs))

