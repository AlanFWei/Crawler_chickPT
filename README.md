# Crawler_chickPT

爬取小雞上工任務列表

目前設定以每 3 秒爬取一次任務頁面，若該網址並未出現在已知中
會將其輸出出來，若不需要串接 Line API 部分，請將 notifyLine 相關刪除即可。

新增 Config 設定 =>
time: 幾秒重整一次
minSalary = 最低薪資
token = Line Token
