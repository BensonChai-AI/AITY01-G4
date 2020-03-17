# In[ ]:

# 資料庫
import psycopg2

database='d1ii52tsb31ga5'
user='vgnorlhadkiiiv'
password='094ca31076b8fcbc09cab98046608aba4bfec2f12ef8bc41c1effcc1937ddf1f'
host='ec2-3-234-109-123.compute-1.amazonaws.com'
port='5432'

def database_init():
    try:
        connection = psycopg2.connect(database=database,
                                      user=user,
                                      password=password,
                                      host=host,
                                      port=port)
        connection.close()
        status = True
    except:
        status = False

    return status

def database_query_columns():
    connection = psycopg2.connect(database = database,
                                  user = user,
                                  password = password,
                                  host = host,
                                  port = port)
    cursor = connection.cursor()

    cursor.execute(f"select column_name,data_type from information_schema.columns where table_name = 'project_data'")
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    connection.commit()
    connection.close()
    return rows

def database_query_pred_img(id):
    connection = psycopg2.connect(database = database,
                                  user = user,
                                  password = password,
                                  host = host,
                                  port = port)
    cursor = connection.cursor()

    cursor.execute(f"select img_name_pred from project_data where id = {id}")

    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    connection.commit()
    connection.close()
    return rows

def database_insert_data(line_name, line_id, address, latitude, longitude, img_name_ori, upload_date):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO project_data (line_name, line_id, address, latitude, longitude, img_name_ori, upload_date) \
                   VALUES ('{line_name}', \
                   '{line_id}', \
                   '{address}', \
                   {latitude}, {longitude}, \
                   '{img_name_ori}', \
                   '{upload_date}') RETURNING id")
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    connection.commit()
    connection.close()

    # row[0][0] is id
    return rows[0][0]

def database_query_info(id):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    cursor.execute(f"select address, upload_date from project_data where id = {id}")

    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    connection.commit()
    connection.close()

    if len(rows) == 1:
        return ' '.join( ['回報位置:', rows[0][0].rstrip(), '\n回報時間:', str(rows[0][1]), '\n處理狀態:未處理'] )
    else:
        return '查無資料'

def database_query_id_by_user(user_id):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    cursor.execute(f"select id from project_data where line_id = '{user_id}' order by id")
    ids = []
    rows = cursor.fetchall()
    for row in rows:
        # print(row)
        ids.append(str(row[0]))
    connection.commit()
    connection.close()

    if len(ids) == 0:
        return '你尚未有任何回報紀錄'
    else:
        return '你的歷史回報編號: ' + ', '.join(ids)

def database_update_img_byte(column_name, img_name, condition):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    f = open("./images/"+img_name, "rb")
    file_data = psycopg2.Binary(f.read())
    f.close()

    cursor.execute("UPDATE project_data SET " + column_name + " = %s WHERE id = %s", (file_data, condition))
    connection.commit()
    connection.close()

def database_download_img_byte(id):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    cursor.execute(f"select img_name_pred, img_byte_pred from project_data where id = {id}")

    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    connection.commit()
    connection.close()

    f = open('./images/' + rows[0][0].rstrip(), 'wb')
    f.write(rows[0][1])
    f.close()

    return rows[0][0]

def database_update_img_pred_name(img_ori, img_pred):
    connection = psycopg2.connect(database=database,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    cursor = connection.cursor()

    cursor.execute(f"update project_data set img_name_pred = '{img_pred}' where img_name_ori = '{img_ori}'")
    connection.commit()
    connection.close()

# In[ ]:
# 本地端

def images_init():
    # 若images資料夾不存在則新增
    if os.path.isdir('./images') == False:
        os.makedirs('./images')

    if os.path.isdir('./images') == True:
        status = True
    else:
        status = False
        
    return  status

import os
import csv
import json

def csv_init():
    # 產生user_report.csv 紀錄使用者回報照片以及位置
    # 產生users.txt 紀錄所有好友的line id

    # 若user_report.csv不存在則新增檔案並寫好欄位名稱
    if os.path.exists('./user_report.csv') == False:
        with open('./user_report.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['line_name', 'user_id',
                                 'address', 'latitude', 'longitude',
                                 'image_name',
                                 'date'])

    # 若users.txt不存在則新增檔案
    if os.path.exists('./users.txt') == False:
        f = open('./users.txt', 'w')
        f.close()

    if os.path.exists('./user_report.csv') == True and os.path.exists('./users.txt') == True:
        status = True
    else:
        status = False

    return status

def csv_record_user_info(user_info):
    record = 1

    # 取出輸入資訊內的user_id
    user_id = json.loads(user_info)['user_id']

    # 將檔案內所有user_id與輸入比對
    with open("./users.txt", "r") as myfile:
        lines = myfile.readlines()
        for line in lines:
            if user_id == json.loads(line)['user_id']:
                record = 0
                break

    # 檔案內找不到相同user_id才把輸入的記錄下來
    if record  == 1:
        with open("./users.txt", "a") as myfile:
            myfile.write(user_info)
            myfile.write('\n')

def csv_record_report_info(line_name, user_id, address, latitude, longitude, image_name, date):
    with open('./user_report.csv', "a", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow([line_name,
                             user_id,
                             address,
                             latitude,
                             longitude,
                             image_name,
                             date])

# In[ ]:
# AWS S3
import boto3

# 老師教學用的金鑰
# aws_access_key_id='AKIAR4NDUH53IFC4FKEV'
# aws_secret_access_key='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'

# 林冠華AWS的金耀 2020/03/02 開通
aws_access_key_id='AKIAJKLY5UKKCKSQZGOQ'
aws_secret_access_key='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'

# 若指定名稱的 bucket 存在回傳 True, 否則 False
def _bucket_exists(bucket):
  s3 = boto3.resource('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
  return s3.Bucket(bucket) in s3.buckets.all()

def s3_init():
    return _bucket_exists('aiprojects3')


def s3_upload(source_file, target_file):
    # 將圖片上傳到S3
    # 上傳
    # Create an S3 client
    S3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    SOURCE_FILENAME = source_file
    TARGET_FILENAME = target_file
    BUCKET_NAME = 'aiprojectimgori'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, TARGET_FILENAME)

def s3_downloadd(object_file, target_file):
    # 將圖片從S3下載
    # 下載
    S3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    BUCKET_NAME = 'aiprojectimgpred'
    OBJECT_NAME = object_file
    FILE_NAME = target_file
    # print(OBJECT_NAME, FILE_NAME)
    S3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)