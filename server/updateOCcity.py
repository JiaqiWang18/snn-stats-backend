from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    agent = {"User-Agent": "Mozilla/5.0"}
    page = requests.get("https://docs.google.com/spreadsheets/u/3/d/1-dt0LlQaP-yA-koWz3tJzR0urkPvlzbEjmqVwWXA5W8/htmlembed/sheet?gid=0&single=true&widget=false&headers=false&chrome=false", headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    output = dict()
    target_ids = ["0R43", "0R38" ,"0R25", "0R19", "0R28"]
    for id in target_ids:
        raw = [ e.text for e in soup.find("th",{"id":id}).find_next_siblings("td")]
        output[raw[0]] = {"Population": int(raw[2]), "Student":int(raw[4].replace("^","")), "Staff":int(raw[6].replace("^", "")), "Rate":float(raw[-1])}

    print(output)