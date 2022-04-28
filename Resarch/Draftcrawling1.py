import bs4
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import csv 
path = 'C:\\Users\\wonho\\Desktop\\ETC\\chromedriver.exe'
data={}

f = open('write.csv','w', newline='', encoding='utf8')
wr = csv.writer(f)
wr.writerow(['타율','경기수','타석','타수','득점','총안타','2루타','3루타','홈런','루타','타점','도루','희타','희비','4사구','삼진','병살','장타율','출루율','OPS','평균자책점','경기수','승','패','이닝','타자','피안타','피홈런','4사구','탈삼진','실점','자책점','승률','WHIP'])

driver = webdriver.Chrome(path)
driver.get('http://www.korea-baseball.com/record/record/player_record?kind_cd=31')

time.sleep(0.1)
driver.find_element_by_class_name('year').click()
time.sleep(0.1)
driver.find_element_by_css_selector("li[prop='2014']").click()

text = driver.page_source
soup = bs4.BeautifulSoup(text,'html.parser')

time.sleep(0.1)
result2 = soup.find('select',attrs={'name':'club_idx'})
schools=[]

for i in result2.find_all('option'):
    schools.append(i.attrs['value'])
    time.sleep(0.1)
schools.pop(0)
del schools[0:78]

for i in schools:
    time.sleep(0.1)
    driver.find_element_by_class_name('team').click()
    time.sleep(0.1)
    driver.find_element_by_css_selector("li[prop='"+i+"']").click()
   
    time.sleep(0.1)
    text = driver.page_source
    soup = bs4.BeautifulSoup(text,'html.parser')
   
    time.sleep(0.1)
    result = soup.find('select',attrs={'name':'person_no'})
    time.sleep(0.1)
    players=[]
    school = soup.find('option',attrs={'value':i}).text
   
   
    for i in result.find_all('option'):
        time.sleep(0.1)
        players.append(i.attrs['value'])
       
    for i in players:
        infoL=[]
        time.sleep(0.1)
        driver.find_element_by_class_name('type').click()
        time.sleep(0.1)
        driver.find_element_by_css_selector("li[prop='"+i+"']").click()
        time.sleep(0.1)
        driver.find_element_by_class_name('searchBtn').click()
        time.sleep(0.1)
        driver.find_element_by_xpath("//a[contains(text(),'타자기록')]").click()
        time.sleep(0.1)
        text = driver.page_source
        time.sleep(0.1)
        soup = bs4.BeautifulSoup(text,'html.parser')
        time.sleep(0.1)
        name = soup.find('option',attrs={'value':i}).text
        time.sleep(0.1)
        data = soup.find('div',attrs={'class':'sumplus'})
        time.sleep(0.1)
        data2 = data.find('ul').text
        time.sleep(0.1)
        infoL.append(name)
        time.sleep(0.1)
        infoL.append(school)
        time.sleep(0.1)
       
        for i in range(4):
            data2 = data2.replace('\n\n','\n')
        data2 = data2.split('\n')
        time.sleep(0.1)
       
        for i in range(1,len(data2)-1):
            infoL.append(data2[i].split(':')[1].strip())
            time.sleep(0.1)
        time.sleep(0.1)
       
        driver.find_element_by_xpath("//a[contains(text(),'투수기록')]").click()
        time.sleep(0.1)
        text = driver.page_source
        time.sleep(0.1)
        soup = bs4.BeautifulSoup(text,'html.parser')
        time.sleep(0.1)
        data = soup.find('div',attrs={'class':'sumplus'})
        time.sleep(0.1)
        data3 = data.find('ul').text
        time.sleep(0.1)
       
        for i in range(4):
            data3 = data3.replace('\n\n','\n')
            time.sleep(0.1)
        data3 = data3.split('\n')
        time.sleep(0.1)

        for i in range(1,len(data3)-1):
            infoL.append(data3[i].split(':')[1].strip())
        time.sleep(0.1)
           
        wr.writerow(infoL)
        time.sleep(0.1)

f.close()
