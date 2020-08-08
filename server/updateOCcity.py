from datetime import date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import mysql

if __name__ == '__main__':
    #driver = `webdriver.Chrome(executable_path=r'D:\chromedriver.exe')
    #driver.get('https://ochca.maps.arcgis.com/apps/opsdashboard/index.html#/ed75287f88bb4872bc605ca23c638069')
    soup = BeautifulSoup(open("D:\DOWNLOADS\Maps Only - Orange County COVID-19 Dashboard - Mobile and Desktop.html", encoding="utf8"), 'html.parser')
    div = soup.find_all("div", {"class": "external-html"})
    raw = []
    for each in div:
        children = each.findChildren("p", recursive=False)
        for child in children:
            raw.append(child.text.split('-\xa0'))
    processed = []
    for each in raw:
        if(len(each)== 2):
            try:
                number = int(each[1].split(" ")[0].replace(",",""))
                processed.append((each[0],number))
            except Exception:
                continue
    processed = processed[:40]
    print(processed)

    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    sql = "update occities set stats = %s where cityname = %s"
    for cityset in processed:
        cursor.execute(sql,(cityset[1],cityset[0]))
        con.commit()
    con.close()

    #div = soup.find_all("div", {"class": 'maincounter-number'})

