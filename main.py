import time
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
if __name__=="__main__":
    #===CONFIG
    baseUrl = 'https://band.us/'
    keyword = input(">>> 키워드를 입력하세요 :: ")
    url = 'https://band.us/discover/search/'+keyword
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.maximize_window()
    #=========
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="input_search_view90"]').clear()
    driver.find_element_by_xpath('//*[@id="input_search_view90"]').send_keys(keyword+Keys.ENTER)
    time.sleep(2)
    cnt = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/section/div/h1/span').text.strip()
    print(cnt)
    lisLength = 0
    while int(cnt) > lisLength:
        body = driver.find_element_by_css_selector('body')
        bs4 = BeautifulSoup(driver.page_source,'lxml')
        lis = bs4.find('ul',class_='cCoverList _bandListContainer').find_all('li')
        lisLength = len(lis)
        print(lisLength)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
    # 모두 페이지소스에 박혔었을떄
    for li in lis:
        try:
            bandUrl = baseUrl + li.find('a')['href']
            name = li.find('strong',class_='name').find('span').get_text().strip()
            memberCnt = int ( li.find('strong',class_='totalNumber').get_text().strip() )
            if memberCnt > 20:
                print(name,memberCnt,bandUrl)
        except: # 맨마지막 경우
            pass


    """
    header1 = ['이름', 'URL', 'member_count']
    wb = Workbook()
    ws1 = wb.worksheets[0]
    ws1.column_dimensions['A'].width = 30
    ws1.column_dimensions['B'].width = 50
    ws1.column_dimensions['C'].width = 20
    ws1.append(header1)
    # 데이터 삽입
    # itemlist 가 [품명,최저가,링크] 이런식으로 온걸
    # openpyxl 객체 ws1 에 append 시키면 들어감
    for itemlist in datalist:
        ws1.append(itemlist)
    wb.save(keyword + ".xlsx")
    print(">>> 파일저장완료")
    input("엔터키나 아무키를 누르시면 종료됩니다. ")
    """