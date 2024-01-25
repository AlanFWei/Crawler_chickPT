import re
import os
import requests
import configparser

from time import sleep
from bs4 import BeautifulSoup


def readData():
    return [l.splitlines()[0] for l in open("chickpt.txt", 'r').readlines()]


def notifyLine(token, message):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, params=payload)


if __name__ == "__main__":
    if not os.path.exists("config.ini") and not os.path.exists("chickpt.txt"):
        config = configparser.ConfigParser()
        config["Setting"] = {}
        config["Setting"]['time'] = "1"
        config["Setting"]['minSalary'] = "0"
        config["Setting"]['token'] = ""
        with open("config.ini", 'w') as f:
            config.write(f)

        open("chickpt.txt", 'w')

    config = configparser.ConfigParser()
    config.read("config.ini")

    url = "https://www.chickpt.com.tw/cases"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    os.system("cls")
    print(f"小雞上工 監視中，目前是以每 {config['Setting']['time']} 秒檢查一次。")
    try:
        while True:
            existsList = readData()
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            for item in soup.find("ul", {"id": "job-list"}).find_all("li"):
                href = item.find("a").get("href")
                divTag = item.find("div", {"class": "is-blk"})
                title = divTag.find("h2").text.strip()
                contact = divTag.find(
                    "p", {"class": "mobile-job-company"}).text.strip()
                salary = int(
                    re.search(r'\d+', divTag.find("span",
                                                  {"class": "salary"}).text).group()
                )
                if salary < int(config['Setting']['minSalary']):
                    continue
                if href not in existsList:
                    with open("chickpt.txt", 'a') as f:
                        f.write(f"{href}\n")
                        print(
                            f"標題： {title} 價格： 單次{salary}元 聯絡人： {contact}")
                        notifyLine(
                            config['Setting']['token'], f"\n標題： {title}\n價格： 單次{salary}元\n聯絡人： {contact}")
            response.close()
            sleep(float(config['Setting']['time']))
    except Exception as e:
        pass
