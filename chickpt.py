import requests
import os
from time import sleep
from bs4 import BeautifulSoup

TIME = 3

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def readData():
    existsList = []
    with open("chickpt.txt", 'r') as f:
        for line in f.readlines():
            noEnterLine = line.splitlines()[0]
            existsList.append(noEnterLine)
    return existsList


def notifyLine(message):
    token = ""
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, params=payload)


if __name__ == "__main__":
    os.system('cls')
    if not os.path.exists("chickpt.txt"):
        open("chickpt.txt", 'w')
    print(f"小雞上工 監視中，目前是以每 {TIME} 秒檢查一次。")
    while True:
        try:
            url = "https://www.chickpt.com.tw/cases"
            existsList = readData()

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.find("ul", {"id": "job-list"}):
                if type(item.find("a")) is int:
                    continue
                aTag = item.find("a")
                if aTag.get('href') not in existsList:
                    with open(os.path.join(os.path.abspath("."), "chickpt.txt"), 'a') as f:
                        f.write(f"{aTag.get('href')}\n")
                        print(
                            f"標題： {aTag.get('title')} 價格： {aTag.find('span', {'class': 'salary'}).text} 聯絡人： {aTag.find('p', {'class': 'ellipsis-job-company'}).text.strip()}")
                        notifyLine(
                            f"\n標題： {aTag.get('title')}\n價格： {aTag.find('span', {'class': 'salary'}).text}\n聯絡人： {aTag.find('p', {'class': 'ellipsis-job-company'}).text.strip()}")
        except Exception as e:
            notifyLine("發生錯誤，請盡速處理。")
            print(e)
        sleep(TIME)
