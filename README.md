# ftx-api

## Description
透過 Line Notify 獲得每日期現套利收益報告。

## Usage

### All you have to prepare:
1. [Line Notify](https://notify-bot.line.me/zh_TW/) API Key
2. [FTX](https://ftx.com/profile) API Key
3. Python >= Version 3.6 (f-string used)

程式需要修改的地方僅有第 74 - 76 行
```python
LINE_API_KEY = 'LINE_NOTIFY_API_KEY'
subaccount = FtxClient('API_KEY','API_SECRET','SUBACCOUNT_NAME') 
coinlist = ['BTC-PERP','ETH-PERP']
```
- subaccount：第三個參數是子帳戶名稱，如果是在主帳號套利，就只需要FtxClient('API_KEY','API_SECRET')就好。
- coinlist：套利幣種的名稱都放進list，記得加上-PERP。

### Execution
```shell
pip insatll -r requirements.txt
python arbitrage.py
```

### Crontab
```shell
Enviroment: Ubuntu Linux 18.04

crontab -e

# execute the file on 7:59 everyday
00 8 * * * python3 /PATH/arbitrage.py 
```
![image](https://user-images.githubusercontent.com/49953246/111897829-1e4ebb80-8a5d-11eb-8d08-1e514c64759c.png)

