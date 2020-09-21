from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
import mysql

def crawlOCCities():
    options = Options()
    options.headless = True

    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://ochca.maps.arcgis.com/apps/opsdashboard/index.html#/2a169f85c2254dd7b43f95b095208356')
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
        processed = processed[:40]
        print(processed)
        con = mysql.connector.connect(user='admin', password='Jiaqi200218',
                                      host='collegedata.cwfud0qzqwsy.us-east-2.rds.amazonaws.com',
                                      database='snn')
        cursor = con.cursor()
        sql = "update occities set stats = %s where cityname = %s"
        for cityset in processed:
            cursor.execute(sql, (cityset[1], cityset[0]))
            con.commit()
        con.close()

        # div = soup.find_all("div", {"class": 'maincounter-number'})
    finally:
        driver.quit()

if __name__ == '__main__':
   crawlOCCities()


