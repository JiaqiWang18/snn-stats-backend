from server.models import UnitedStates, LACounty, California, OrangeCounty

from sqlalchemy.exc import IntegrityError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import requests
import mysql.connector
import mysql
import os
import pytz

# config vars

if(os.environ.get("DEBUG")):
    GOOGLE_CHROME_PATH = ""
    CHROMEDRIVER_PATH = "D:\chromedriver.exe"
else:
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
DATABASE_URL = os.environ.get("SNN_RDS_URL")
DATABASE_PASS = os.environ.get("SNN_RDS_PASS")
US_SOURCE = os.environ.get("COVID_US_SOURCE")
CA_SOURCE = os.environ.get("COVID_CA_SOURCE")
LA_SOURCE = os.environ.get("COVID_LA_SOURCE")
OC_SOURCE = os.environ.get("COVID_OC_SOURCE")
OCCITIES_SOURCE = os.environ.get("COVID_OCCITIES_SOURCE")
USER_AGENT = {"User-Agent": "Mozilla/5.0"}


def crawl_us(link):
    try:
        page = requests.get(link, headers=USER_AGENT)
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all("div", {"class": 'maincounter-number'})
        raw = list()
        for each in div:
            children = each.findChildren("span", recursive=False)
            for child in children:
                raw.append(int(child.text.replace(",", "")))
        return {
            "united_states":
                {
                    "total_cases": raw[0],
                    "death": raw[1],
                    "recovered": raw[2]
                }
        }

    except Exception as err:
        return {
            "US Crawler Error": err,
        }


def crawl_ca(link):
    try:
        page = requests.get(link, headers=USER_AGENT)
        soup = BeautifulSoup(page.content, 'html.parser')
        each = soup.find_all("div", {"class": 'big-number'})[:2]
        each = [int(info.text.replace(",", "")) for info in each]
        return {"california": {
            "total_cases": each[0],
            "death": each[1]
        }}
    except Exception as err:
        return {
            "CA Crawler Error": err,
        }


def crawl_la(link):
    try:
        page = requests.get(link, headers=USER_AGENT)
        soup = BeautifulSoup(page.content, 'html.parser')
        td = soup.find_all("td")
        raw = [info.text.replace(",", "") for info in td]
        data = {}

        for i in range(6, 20):
            print(str(i) + ":" + str(raw[i]))

            if ("Laboratory Confirmed Cases" in raw[i]):
                data["total_cases"] = int(raw[i + 1])
            elif ("Deaths" in raw[i]):
                data["death"] = int(raw[i + 1])
                break
        if (len(data) != 2):
            raise Exception("La crawling error")
        return {"la_county": data}
    except Exception as err:
        return {
            "LA County Crawler Error": err,
        }


def crawl_oc(link):
    try:
        page = requests.get(link, headers=USER_AGENT)
        soup = BeautifulSoup(page.content, 'html.parser')
        each = soup.find_all("h3", {"class": 'casecount-panel-title'})
        each = [info.text.replace(",", "").replace("*", "") for info in each]
        if (len(each) != 9):
            raise Exception("OC crawling error")
        return {"orange_county": {
            "total_cases": int(each[0]),
            "death": int(each[2]),
            "total_tested": int(each[4]),
        }}
    except Exception as err:
        return {
            "Orange County Crawler Error": err,
        }


def update_oc_cities():
    options = webdriver.ChromeOptions()
    options.binary_location = GOOGLE_CHROME_PATH
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(OCCITIES_SOURCE)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ember273"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find_all("div", {"class": "external-html"})
        raw = []
        for each in div:
            children = each.findChildren("p", recursive=False)
            for child in children:
                raw.append(child.text.split('-\xa0'))
        processed = []
        for each in raw:
            if (len(each) == 2):
                try:
                    number = int(each[1].split(" ")[0].replace(",", ""))
                    processed.append((each[0], number))
                except Exception:
                    continue
        processed = processed[:41]
        con = mysql.connector.connect(user='admin', password=DATABASE_PASS,
                                      host=DATABASE_URL,
                                      database='covid_data')
        cursor = con.cursor()
        pacific_time = pytz.timezone('US/Pacific')
        current_date = datetime.now(pacific_time).date()
        cursor.execute("SELECT * FROM oc_cities WHERE date=%s", (current_date,))
        exists = cursor.fetchall()
        if(len(exists) == 0):
            sql = "INSERT INTO oc_cities (date, "
            for tup in processed:
                processed_city_name = tup[0].lower().replace(" ", "_")
                sql += processed_city_name[:-1] + ", "

            sql = sql[:-2] + ") VALUES (%s, "
            for tup in processed:
                data = tup[1]
                sql += f"{data}, "
            sql = sql[:-2] + ");"
            cursor.execute(sql, (current_date,))
            con.commit()
        else:
            sql = "UPDATE oc_cities SET "
            for tup in processed:
                processed_city_name = tup[0].lower().replace(" ", "_")
                sql += f"{processed_city_name[:-1]} = {tup[1]}, "
            sql = sql[:-2] + " WHERE date = %s;"
            cursor.execute(sql, (current_date,))
            con.commit()
        con.close()
        return (processed)
    finally:
        driver.quit()

# this function will create a new row if there is no data entry with the current date, otherwise it will update the row
def store_to_db():
    from server import db

    con = mysql.connector.connect(user='admin', password=DATABASE_PASS,
                                  host=DATABASE_URL,
                                  database='snn')
    cursor = con.cursor()
    # get parsed data from crawling functions
    data = {}
    data.update(crawl_us(US_SOURCE))
    data.update(crawl_ca(CA_SOURCE))
    data.update(crawl_la(LA_SOURCE))
    data.update(crawl_oc(OC_SOURCE))

    pacific_time = pytz.timezone('US/Pacific')
    current_date = datetime.now(pacific_time).date()
    query = lambda table_name: db.session.query(table_name).get(current_date)

    for key in data.keys():
        if (key == "united_states"):
            if(not query(UnitedStates)):
                db.session.add(
                    UnitedStates(date=current_date, total_cases=data[key]["total_cases"], death=data[key]["death"],
                                 recovered=data[key]["recovered"]))
            else:
                updateQuery(UnitedStates, data[key])

        elif (key == "california"):
            if (not query(California)):
                db.session.add(
                    California(date=current_date, total_cases=data[key]["total_cases"], death=data[key]["death"]))
            else:
                updateQuery(California, data[key])

        elif (key == "la_county"):
            if (not query(LACounty)):
                db.session.add(LACounty(date=current_date, total_cases=data[key]["total_cases"], death=data[key]["death"]))
            else:
                updateQuery(LACounty, data[key])

        elif (key == "orange_county"):
            if (not query(OrangeCounty)):
                db.session.add(
                    OrangeCounty(date=current_date, total_cases=data[key]["total_cases"], death=data[key]["death"],
                                 total_tested=data[key]["total_tested"]))
            else:
                updateQuery(OrangeCounty, data[key])
    db.session.commit()

def updateQuery(obj, dic):
    for key, value in dic.items():
        setattr(obj, key, value)

if __name__ == '__main__':
    print(update_oc_cities())
