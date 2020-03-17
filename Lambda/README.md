# 申請 AWS 帳號後須綁定一張信用卡才能使用免費方案  
  
# 進入主控台選擇 Lambda  
# 點選建立函式  
# 取名  
# 選擇 Python 3.6  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%201.png)  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%202.png)  
  
# 進入函式  
# 點選 Layer    
# 點選新增 Layer  
# 選擇 "提供 Layer 版本 ARN" 輸入紅框內ARN 或參考 https://github.com/antonpaquin/Tensorflow-Lambda-Layer/tree/master/arn_tables  
# 點選新增觸發條件  
# 選擇 API Geteway  
# 選擇 建立新的 API  
# 新增  
  
# 點選新增觸發條件  
# 選擇 S3  
# 設定 儲存貯體 為 aiprojectimgori  
# 新增  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%203.png)  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%204.png)  
  
# 使用 zip 上傳 "上傳\主程式與其他使用zip上傳\setup.zip"  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%206.png)  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%205.png)  
  
# 調整記憶體大小與逾時  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%207.png)  
  
# 將 "上傳\套件與模型傳至S3" 內的兩個檔案上傳至 S3 的 aiprojects3 儲存貯體
  
檔案說明:  
先準備套件，要先自行將要用到的套件下載至資料夾，這個專題有三個套件要自己額外安裝  
matplotlib: 去下載 linux 的 whl 檔案安裝，然後安裝到 "套件\"  
kiwisolver: 去下載 linux 的 whl 檔案安裝，然後安裝到 "套件\"  
psycopg2: 直接下載到 "套件\"，有人準備好了https://github.com/jkehler/awslambda-psycopg2  
  
將 "套件\awslambda-psycopg2-master\with_ssl_support\psycopg2-3.6" 複製出來因為我們要用這版本  
將 "套件\kiwisolver_linux\" 跟 "套件\matplotlib_linux\" 複製放到 "lambda-requirements\" 然後直接 zip 上傳至 S3 的 aiprojects3 儲存貯體  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%208.png)  
將 模型權重檔 trained_weights_final.h5 上傳至 S3 的 aiprojects3 儲存貯體  
(trained_weights_final.h5 檔案太大無法上傳github，請從其他方式取得)
將下圖檔案一起 zip 後，使用 zip 上傳到 lambda，然後切換成 編輯內嵌程式碼，可以查看編輯  
![image](https://github.com/broodkey/AITY01-G4/blob/master/Lambda/md_images/MD%209.png)  
font\, model_data\, yolo3\, detect.py:是 yolo3 的測試函式  
lambda_function.py: 主程式  
setup.py: 主程式啟動時候會去 S3 下載 lambda-requirements.zip 跟 trained_weights_final.h5  

# 備註:
程式內沒有放 S3 金鑰，請改成自己的，不要把金鑰放在程式內上傳 github，AWS 可以檢查得到，然後寄信給你說你的金鑰很危險  
同理 Postgres 的設定也改成自己的，雖然不會被檢查  
Lambda 應該可以使用不需設定金鑰也能直接存取自己 S3，因為每個儲存貯體都是唯一的，但似乎要經過一些設定
因為儲存貯體名稱是絕對唯一，因此上面範例所填寫的儲存貯體請依照自己的 S3 修改
