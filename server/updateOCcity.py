import smtplib, ssl, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_func():
    LINK="https://www.dhl.com/us-en/home/tracking/tracking-express.html?submit=1&tracking-id=6266743836"
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.binary_location = GOOGLE_CHROME_PATH
    #options.add_argument("--headless")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")

    #driver = webdriver.Chrome(executable_path="D:\DOWNLOADS\chromedriver_win32 (1)\chromedriver.exe")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    driver.get(LINK)
    try:
        element = WebDriverWait(driver, random.randrange(20,25)).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-tracking-result--status-copy-message"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.find_all("h3", {"class": "c-tracking-result--status-copy-message"})

        target = [each.text for each in result]
        print(target)
        if("not yet picked up" not in target[0]):
            send(target[0])
        return target
    finally:
        driver.quit()

def send(message):
    port = 465  # For SSL
    context = ssl.create_default_context()
    EMAIL_ADDRESS = "jacky200218@gmail.com"
    EMAIL_PASS = "nmsxsyktuzdrdqze"
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASS)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

if __name__ == '__main__':
  print(test_func())
