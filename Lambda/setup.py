import boto3
import os
import sys
import zipfile
import glob

# 用來計數被觸發幾次
count = 0

# ----------
# 套件上傳方式1 (有大小限制 連同主程式不能超過50MB)
# 將套件安裝在資料夾內 (需要配合 amazon linux 安裝 linux 版本)
# zip 減少大小
# 使用 zip 上傳後用這邊的程式碼解壓縮
#  ----------
# pkgdir = '/tmp/requirements'
# zip_requirements = 'lambda-requirements.zip'

# if os.environ.get("AWS_EXECUTION_ENV") is not None:
#     if not os.path.exists(pkgdir):
#         root = os.environ.get('LAMBDA_TASK_ROOT', os.getcwd())
#         zip_requirements = os.path.join(root, zip_requirements)
#         zipfile.ZipFile(zip_requirements, 'r').extractall(pkgdir)

#         for p in glob.glob(pkgdir + '/lambda-requirements/*'):
#             sys.path.append(p)

# ----------
# 套件上傳方式2
# 將套件安裝在資料夾內 (需要配合 amazon linux 安裝 linux 版本)
# zip 減少大小
# 上傳至 S3
# 從 S3 下載之後解壓縮
# ----------
# AWS的金鑰 (請勿寫在 code 裡面上傳 github)
aws_access_key_id=''
aws_secret_access_key=''

REQUIREMENTS_BUCKET_NAME = 'aiprojects3'
REQUIREMENTS_KEY = 'lambda-requirements.zip'

pkgdir = '/tmp/requirements'
zip_requirements = '/tmp/lambda-requirements.zip'

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    if not os.path.exists(pkgdir):
        print(pkgdir, '不存在')

        print('從s3下載', REQUIREMENTS_KEY)
        s3 = boto3.resource('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
        bucket = s3.Bucket(REQUIREMENTS_BUCKET_NAME)
        bucket.download_file(REQUIREMENTS_KEY, zip_requirements)
        print('下載完成')

        print('解壓縮', zip_requirements, '->', pkgdir)
        zipfile.ZipFile(zip_requirements, 'r').extractall(pkgdir)
        print('刪除', zip_requirements)
        os.remove(zip_requirements)
        for p in glob.glob(pkgdir + '/lambda-requirements/*'):
            sys.path.append(p)

# ----------
# 使用與套件上傳方式2相同方法上傳模型權重檔
# 檔案如果超過 125MB的話不能壓縮
# 因為 /tmp 僅允許250MB大小，如果你放了一個200MB的壓縮檔，解壓縮的時後空間會爆掉
# 上傳至 S3
# 從 S3 下載之後解壓縮
# ----------
MODEL_BUCKET = 'aiprojects3'
key = 'trained_weights_final.h5'
local_path = os.path.join('/tmp', key)
if not os.path.isfile(local_path):
    print(key, '不存在本地端')

    print('下載路徑:', local_path)
    s3 = boto3.resource('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(MODEL_BUCKET)
    bucket.download_file(key, local_path)
    print(key, '從S3下載至本地端')
else:
    print(key, '已存在本地端')
