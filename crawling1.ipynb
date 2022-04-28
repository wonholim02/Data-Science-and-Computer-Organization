path = 'C:\\Users\\wonho\\Desktop\\ETC\\chromedriver.exe'
driver = webdriver.Chrome(path)

f2 = open('write2.csv','w', newline='', encoding='utf8')
wr = csv.writer(f2)

driver.get('https://ko.wikipedia.org/wiki/KBO_%EB%A6%AC%EA%B7%B8_%EC%8B%A0%EC%9D%B8_%EB%93%9C%EB%9E%98%ED%94%84%ED%8A%B8')
years = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
text3 = driver.page_source
soup3 = bs4.BeautifulSoup(text3,'html.parser')

for i in years:
    y = str(i)
    time.sleep(0.1)
    driver.find_element_by_xpath("//a[contains(text(),"+y+")]").click()
    time.sleep(0.1)
    infoL2=[]
   
    text2 = driver.page_source
    soup2 = bs4.BeautifulSoup(text2,'html.parser')
    time.sleep(0.1)
    result2 = soup2.find_all('a',attrs={'class':"new"})

    for i in result2:
        name = i.text
        infoL2.append(name)

    infoL22=infoL2[0:len(infoL2)-8]
   
    wr.writerow(infoL22)
   
    time.sleep(0.1)
   
    driver.get('https://ko.wikipedia.org/wiki/KBO_%EB%A6%AC%EA%B7%B8_%EC%8B%A0%EC%9D%B8_%EB%93%9C%EB%9E%98%ED%94%84%ED%8A%B8')
   
f2.close()
