import boto3
import json
import glob
from PIL import Image
import setup
import detect
import psycopg2
import time


def lambda_handler(event, context):
    # print(event)
    print('--- 觸發次數:', setup.count, '---')
    setup.count += 1

    if 'resource' in event:
        print('API 觸發')
        t1 = time.time()
        yolo = detect.load_yolo('yolo')
        t2 = time.time()
        print('載入yolo使用:', t2 - t1, 's')
        if setup.count != 1:
            print('-睡10秒-')
            time.sleep(10)
        return {
            'statusCode': 200,
            'body': json.dumps('API ok')
        }
    else:
        print('S3 觸發')
        # 取得上傳到s3的檔名
        # print(event['Records'][0]['s3']['object']['key'])
        img_ori = event['Records'][0]['s3']['object']['key']
        img_pred = img_ori.replace('ori', 'pred')

        # 將檔案下載至 /tmp
        # AWS的金鑰 (請勿寫在 code 裡面上傳 github)
        aws_access_key_id = ''
        aws_secret_access_key = ''
        S3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        OBJECT_NAME = img_ori
        FILE_NAME = '/tmp/' + img_ori
        BUCKET_NAME = 'aiprojectimgori'
        S3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)

        # 偵測
        yolo = detect.load_yolo('yolo')
        image = Image.open('/tmp/' + img_ori)
        pred_image = yolo.detect_image(image)
        pred_image.save('/tmp/' + img_pred)

        # 將結果上傳至 s3
        S3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        SOURCE_FILENAME = '/tmp/' + img_pred
        TARGET_FILENAME = img_pred
        BUCKET_NAME = 'aiprojectimgpred'
        S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, TARGET_FILENAME)

        # 將結果檔名寫入 postgresql
        database = ''
        user = ''
        password = ''
        host = ''
        port = ''

        connection = psycopg2.connect(database=database,
                                      user=user,
                                      password=password,
                                      host=host,
                                      port=port)
        cursor = connection.cursor()

        cursor.execute(
            f"update project_data set img_name_pred = '{img_pred}' where img_name_ori = '{img_ori}'")
        connection.commit()
        connection.close()

        return {
            'statusCode': 200,
            'body': json.dumps('S3')
        }