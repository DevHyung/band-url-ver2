import time
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


if __name__=="__main__":
    # 20180725 16:42
    now = 1532504559.5943735
    terminTime = now + 60 * 60 * 3
    print("체험판 만료기간 : ", time.ctime(terminTime))
    if time.time() > terminTime:
        print('만료되었습니다.')
        exit(-1)

    #===CONFIG
    wb = Workbook()
    ws1 = wb.worksheets[0]
    header1 = ['이름', 'URL', 'member_count']
    ws1.column_dimensions['A'].width = 30
    ws1.column_dimensions['B'].width = 50
    ws1.column_dimensions['C'].width = 20
    ws1.append(header1)

    keyword = input(">>> 키워드를 입력하세요 :: ")
    min = int( input(">>> Min ~ MAX 멤버수중 Min값을 입력하세요(포함) :") )
    max = int(input(">>> {} ~ MAX 멤버수중 Min값을 입력하세요(포함) :".format(min)))
    print(">>> {} ~ {} 멤버밴드만 추출을 시작합니다.".format(min,max))
    baseUrl = 'https://band.us/'
    url = 'https://band.us/discover/search/'+keyword
    driver = webdriver.Chrome('chromedriver')
    driver.maximize_window()
    #=========
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="input_search_view90"]').clear()
    driver.find_element_by_xpath('//*[@id="input_search_view90"]').send_keys(keyword+Keys.ENTER)
    time.sleep(2)
    cnt = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/section/div/h1/span').text.strip()
    print(">>> 총 검색 갯수 : ",cnt)
    lisLength = 0
    while int(cnt) > lisLength:
        body = driver.find_element_by_css_selector('body')
        bs4 = BeautifulSoup(driver.page_source,'lxml')
        lis = bs4.find('ul',class_='cCoverList _bandListContainer').find_all('li')
        lisLength = len(lis)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
    # 모두 페이지소스에 박혔었을떄
    print(">>> 검색완료 추출 시작")
    for li in lis:
        try:
            bandUrl = baseUrl + li.find('a')['href']
            name = li.find('strong',class_='name').find('span').get_text().strip()
            memberCnt = int ( li.find('strong',class_='totalNumber').get_text().strip() )
            if min <= memberCnt <= max:
                ws1.append([name,bandUrl,memberCnt])
        except: # 맨마지막 경우
            pass
    print(">>> 추출완료 파일저장중")
    wb.save(keyword + ".xlsx")
    driver.quit()
    input("완료되었습니다. ")

