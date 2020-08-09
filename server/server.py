from flask import Flask, request, jsonify,render_template
from datetime import date, timedelta
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests
import mysql.connector
import mysql

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD']=True
CORS(app)

def crawlUS(link):
    agent = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(link, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find_all("div", {"class": 'maincounter-number'})
    raw = list()
    for each in div:
        children = each.findChildren("span", recursive=False)
        for child in children:
            raw.append(int(child.text.replace(",","")))

    if(len(raw)!=3):
        raise Exception("US crawling exception")
    return {
        "US Total Cases （美国总共）":raw[0],
        "US Deaths （美国死亡）":raw[1],
        "US Recovered （美国康复）":raw[2]
    }

def crawlCa(link):
    agent = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(link, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    each = soup.find_all("div", {"class": 'big-number'})
    each = [int(info.text.replace(",","")) for info in each]
    if (len(each) != 2):
        raise Exception("CA crawling exception")
    return {
        "CA Total （加州总共）":each[0],
        "CA Deaths （加州死亡）":each[1]
    }

def crawlLa(link):
    agent = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(link, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    td = soup.find_all("td")
    raw = [info.text.replace(",","") for info in td]
    data = {}

    for i in range(6,20):
        print(str(i)+":"+str(raw[i]))

        if("Laboratory Confirmed Cases" in raw[i]):
            data["LA Total （洛杉矶县总共）"] = int(raw[i+1])
        elif("Deaths" in raw[i]):
            data["LA Deaths （洛杉矶县死亡）"] = int(raw[i + 1])
            break
    if(len(data)!=2):
        raise Exception ("La crawling error")
    return data

def crawlOC(link):
    agent = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(link, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    each = soup.find_all("h3", {"class": 'casecount-panel-title'})
    each = [info.text.replace(",","").replace("*","") for info in each]
    if(len(each)!=9):
        raise Exception("OC crawling error")
    return {
        "OC Total （橙县总共）":int(each[0]),
        "OC Increase （橙县新增）":int(each[1]),
        "OC Death （橙县死亡）":int(each[2]),
        "OC Death Increase （橙县新增死亡）":int(each[3]),
        "OC ICU（橙县ICU病例）": int(each[7]),
        "OC Total Tested （橙县已检测）":int(each[4]),
        "OC Hospitalized （橙县住院人数）":int(each[6]),
    }

def updateYesterday():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM currentStats")
    current = cursor.fetchall()
    for dataset in current:
        sql = "UPDATE yesterdayStats SET Stats = %s WHERE Label = %s;"
        cursor.execute(sql,(dataset[2],dataset[1]))
        con.commit()
    con.close()

def updateYesterOC():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    sql = "SELECT * FROM occities"
    cursor.execute(sql)
    current = cursor.fetchall()
    print(current)
    sql = "update yesteroc set stats = %s where cityname = %s"
    #sql = "insert into yesteroc (cityname,stats) values (%s,%s)"
    for cityset in current:
        cursor.execute(sql, (cityset[1], cityset[0]))
        con.commit()
    con.close()

def updateLog():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM currentStats")
    current = cursor.fetchall()
    dt = date.today() - timedelta(days=1)
    monthdate = float(str(dt.month)+"."+str(dt.day))
    cursor.execute(f"SELECT Date FROM logs WHERE Date = {monthdate}")
    checker = cursor.fetchall()
    print(checker)
    if(len(checker)==0):
        cursor.execute(("INSERT INTO logs (Date) VALUES (%s)"), (monthdate,))
        con.commit()
        for sub in current:
            sql = f"UPDATE logs SET `{sub[1]}` = {sub[2]} WHERE Date = {monthdate}"
            cursor.execute(sql)
            con.commit()
    con.close()

@app.route('/')

def index():
    return render_template("covidstats.html")

@app.route('/snnfrontpage')
def snnfront():
    return render_template("frontpage.html")

@app.route('/crawlData')
def crawlData():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    data = [
        crawlUS("https://www.worldometers.info/coronavirus/country/us/"),
        crawlCa("https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/"),
        crawlLa("http://www.publichealth.lacounty.gov/media/Coronavirus/locations.htm"),
        crawlOC("https://occovid19.ochealthinfo.com/coronavirus-in-oc")
    ]

    counter = 1
    for sub in data:
        for  key in sub:
            sql = "UPDATE currentStats SET Stats = %s WHERE Label = %s"
            val = (sub[key],key)
            cursor.execute(sql, val)
            con.commit()
            counter+=1
    con.close()
    return jsonify(data)

@app.route('/getData')
def getData():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM currentStats")
    current = cursor.fetchall()
    cursor.execute("SELECT * FROM yesterdayStats")
    yesterday = cursor.fetchall()

    if(len(current)-len(yesterday))!=0:
        raise Exception("unequal database")
    output=dict()
    for i in range(len(current)):
        output[current[i][1]] = [current[i][2], current[i][2]-yesterday[i][2]]
    print(output)
    #output["OC Today Percentage of Positive Cases （橙县今日检测阳性概率）"] = [round(output['OC Total （橙县总共）'][1]/output['OC Total Tested （橙县已检测）'][1],3) ,0]

    cursor.execute("SELECT * FROM occities")
    occurrent = cursor.fetchall()
    cursor.execute("SELECT * FROM yesteroc")
    ocyesterday = cursor.fetchall()
    for i in range(len(occurrent)):

        output[occurrent[i][0]] = [occurrent[i][1], occurrent[i][1]-ocyesterday[i][1]]
    con.close()
    return jsonify(output)

@app.route('/updateYesterday')

def setYesterday():
    updateYesterday()
    updateLog()
    updateYesterOC()
    return "working"

@app.route("/graphData")
def getGraphData():
    con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                  host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                  database='snn')
    cursor = con.cursor()
    sql = "SELECT * FROM logs ORDER BY Date ASC"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM currentStats")
    current = cursor.fetchall()
    print(data)
    dt = date.today()
    monthdate = float(str(dt.month) + "." + str(dt.day))
    output = {}
    for row in data:
        output[float(row[0])]=[row[1],row[4],row[6],row[8]]
    output[monthdate]=[current[0][2],current[3][2],current[5][2],current[7][2]]


    con.close()
    return jsonify(output)

if __name__ == '__main__':
    #crawlOCCity("https://ochca.maps.arcgis.com/apps/opsdashboard/index.html#/cc4859c8c522496b9f21c451de2fedae")
    #updateYesterOC()
    print(crawlLa("http://www.publichealth.lacounty.gov/media/Coronavirus/locations.htm"))
