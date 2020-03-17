Line Chat Bot

1. 創建 line bot channel  
不另贅述  
  
2. 設定line_secret_key  
channel_access_token 填寫成 line channel 的 Channel access token  
secret_key 填寫成 line channel 的 Channel secret  
self_user_id 填寫成 line channel 的 Your user ID  
rich_menu_id 稍後上傳 rich menu 後再填寫  
server_url 佈署時填寫  
  
3. 上傳 rich menu  
依序執行 Step1_UserRichMenu.ipynb 到 set_rich_menu_image 完成即可  
另外將 create_rich_menu 的回傳印出填寫到 line_secret_key 的 rich_menu_id  
  
4. 本機測試 by ngrok  
啟動 ngrok 後取得網址 如:https://03bbd375.ngrok.io  
將其填寫至line bot channel 設定的 Webhook URL  
將網址的 03bbd375.ngrok.io 填入 line_secret_key 的 server_url  
  
5. 執行 app.py  
若不想使用 PostgreSQL 請將 app.py 的 local_mode 內關於 PostgreSQL 的 code 註解  
啟動後加入 line 頻道進行測試  
由於上傳檔案限制 trained_weights_final.h5 無法上傳至 github 請組員自行放至此路徑下  
  
6. 檔案說明:  
Step1_UserRichMenu.ipynb 與 rich_menu_images/: 用來上傳(或修改刪除)圖文選單  
QRcode/: 放 QR code 圖檔，用於分享好友的三個方式之一  
demo_images/: 放的是使用者輸入 "測試" 的時候給測試圖片  
yolo3_test/: yolo3 測試程式  
Procfile, requirements.txt, runtime.txt: 部屬至 Heroku 的時候需要的設定檔  
my_database.py: 存取 PostgreSQL, S3 及本地端檔案 (裡面相關設定跟金鑰等已移除，請根據自己的填寫)  
app.py, line_secret_key: Line Chat Bot主程式即設定檔  
套件.txt: 套件版本說明  
  
備註: AWS 的金鑰不要寫在 code 裡面上傳到 github，會被 Amazon 偵測到寄信通知
