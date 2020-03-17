申請 AWS 帳號後須綁定一張信用卡才能使用免費方案

進入主控台選擇 Lambda
點選創建函式
取名 選擇 Python 3.6

進入函式
點選 Layer 
點選新增 Layer
使用 提供 Layer 版本 ARN 輸入框內數字 或參考 https://github.com/antonpaquin/Tensorflow-Lambda-Layer/tree/master/arn_tables
點選新增觸發條件
新增 API Geteway
選擇 建立新的 API
新增

點選新增觸發條件
新增 S3
設定 儲存貯體 為 aiprojectimgori
新增

使用 zip 上傳
上傳\主程式與其他使用zip上傳\setup.zip

將 上傳\套件與模型傳至S3 內兩個檔案上傳至 S3 的 aiprojects3 儲存貯體

檔案說明:
先準備套件，要先自行將要用到的套件下載至資料夾，這個專題有三個套件要自己額外安裝
matplotlib 去下載 linux 的 whl 檔案安裝
kiwisolver 去下載 linux 的 whl 檔案安裝
psycopg2 有人準備好了https://github.com/jkehler/awslambda-psycopg2

將 套件\awslambda-psycopg2-master\with_ssl_support\psycopg2-3.6 複製出來因為我們要用這版本
將 套件\kiwisolver_linux\ 跟 套件\matplotlib_linux\ 複製放到 lambda-requirements\ 然後直接 zip 上傳至 S3 的 aiprojects3 儲存貯體
將 模型權重檔 trained_weights_final.h5 上傳至 S3 的 aiprojects3 儲存貯體
將下圖一起 zip 後 使用 zip 上傳到 lambda
font\ model_data\ yolo3\ detect.py 是 yolo3 的測試函式
lambda_function.py 為主程式
setup.py是主程式啟動時候回去 S3 下載 lambda-requirements.zip 跟 trained_weights_final.h5
