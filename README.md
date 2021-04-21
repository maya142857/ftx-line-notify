# ftx-api

## Description
透過 Line Notify 獲得每日期現套利收益報告，有每日和每小時兩種版本，效果如下圖。

<img src="https://github.com/maya142857/ftx-line-notify/blob/main/.img/per-day.png" height="100" width="50">

## 使用說明

### All you have to prepare:
1. [Line Notify API Key](https://notify-bot.line.me/zh_TW/)：到網站申請一組API_KEY，並連結到你要接收通知的聊天室
2. [FTX API Key](https://ftx.com/profile)：需要一組能夠讀取到套利子帳戶的API KEY，唯獨權限即可。
3. [Python](https://www.python.org/)：程式有使用到f-string，請安裝 >=3.6 的Python版本。
4. [pip](https://pip.pypa.io/en/stable/installing/)：Python套件管理工具。

--- 
### Coding
程式需要修改的地方僅有第 74 - 76 行
```python
LINE_API_KEY = 'LINE_NOTIFY_API_KEY'
subaccount = FtxClient('API_KEY','API_SECRET','SUBACCOUNT_NAME') 
coinlist = ['BTC-PERP','ETH-PERP']
```
- subaccount：第三個參數是子帳戶名稱，如果是在主帳號套利，就只需要FtxClient('API_KEY','API_SECRET')就好。
- coinlist：套利幣種的名稱都放進list，記得加上-PERP。

### Execution
完成上述修改後，到python檔案的目錄下，開啟命令提示字元(cmd)，輸入以下兩行指令就大功告成了。
```shell
pip install requests
python arbitrage.py
```
--- 
### Crontab
你需要一台24小時開機的主機，設定在每小時/每日，自動執行一次Python程式。

#### Linux
```shell
Enviroment: Ubuntu Linux 18.04

crontab -e

# execute the file on 8:00 everyday
00 8 * * * python3 /PATH/arbitrage.py 
```

#### Windows
- 開始→工作排程器→右邊工作排程器程式庫欄位→新增工作
- 一般欄位，名稱隨便取，你記的住就好，重點是觸發程序、動作的部分
- <img src="https://github.com/maya142857/ftx-line-notify/blob/main/.img/win-crontab(1).png" height="120" width="100">
- <img src="https://github.com/maya142857/ftx-line-notify/blob/main/.img/win-crontab(2).png" height="120" width="100">
- 程式或指令碼：輸入你python.exe的檔案位置 (example. C:\Users\user\AppData\Local\Programs\Python\Python38-32\python.exe)。
- 新增引數：輸入arbitrage.py的檔案位置 (example. C:\Users\user\Desktop\printhi.py)。
- 完成後可以直接點右邊的執行，測試看看是否設定正確
- <img src="https://github.com/maya142857/ftx-line-notify/blob/main/.img/win-crontab(3).png" height="80" width="50">

--- 
### 常見問題
1. 如果沒有IDE，怎麼修改Python程式：對arbitrage.py點右鍵→開啟檔案→記事本。
2. [安裝ciso8601失敗](https://hjwang520.pixnet.net/blog/post/404280185-%E5%AE%89%E8%A3%9Dmicrosoft-visual-c%2B%2B-14.0)：因為這個套件是使用C++撰寫，點進去超連結安裝Microsoft Visual C++ 14.0後，再安裝ciso8601套件應該就沒問題了。
3. 如果需要什麼額外的功能，可以直接參考官方的[API Documentation](https://docs.ftx.com/#overview)。
