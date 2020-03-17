#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, LocationMessage, QuickReply, QuickReplyButton, PostbackAction
)

# 引入所需要的消息與模板消息
from linebot.models import (
    MessageEvent, TemplateSendMessage , PostbackEvent
)

# 引入按鍵模板
from linebot.models.template import(
    ButtonsTemplate
)

# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入json處理套件
import json

# 資料庫
import my_database

import os
import time
import pytz
import datetime

import requests

# local or depoly
SET_DEPOLY_MODE = 'local'

if SET_DEPOLY_MODE == 'local':
    import sys
    sys.path.append('./yolo3_test')
    from yolo3_test import detect

# In[ ]:

# 載入基礎設定檔
secretFileContentJson=json.load(open("line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/" , static_folder = "./")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# In[ ]:

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# In[ ]:

# 按鍵訊息
ButtonsTemplateJsonString_Image = """
{
  "type": "template",
  "altText": "this is a buttons template",
  "template": {
    "type": "buttons",
    "actions": [
      {
        "type": "uri",
        "label": "上傳照片",
        "uri": "line://nv/cameraRoll/single"
      },
      {
        "type": "uri",
        "label": "立即拍攝",
        "uri": "line://nv/camera/"
      }
    ],
    "title": "道路坑洞回報",
    "text": "請上傳照片"
  }
}
"""
ButtonsTemplate_Image = TemplateSendMessage.new_from_json_dict(json.loads(ButtonsTemplateJsonString_Image))

ButtonsTemplateJsonString_Location = """
{
  "type": "template",
  "altText": "this is a buttons template",
  "template": {
    "type": "buttons",
    "actions": [
      {
        "type": "uri",
        "label": "定位回報",
        "uri": "line://nv/location"
      },
      {
        "type": "message",
        "label": "手動回報(尚未實現)",
        "text": "[bot]尚未實現"
      }
    ],
    "title": "道路坑洞回報",
    "text": "請回報位置"
  }
}
"""
ButtonsTemplate_Location = TemplateSendMessage.new_from_json_dict(json.loads(ButtonsTemplateJsonString_Location))

ButtonsTemplateJsonString_Confirm = """
{
  "type": "template",
  "altText": "this is a buttons template",
  "template": {
    "type": "buttons",
    "actions": [
      {
        "type": "message",
        "label": "確認回報",
        "text": "[bot]確認回報"
      },
      {
        "type": "message",
        "label": "放棄回報",
        "text": "[bot]放棄回報"
      }
    ],
    "title": "道路坑洞回報",
    "text": "完成"
  }
}
"""
ButtonsTemplate_Confirm = TemplateSendMessage.new_from_json_dict(json.loads(ButtonsTemplateJsonString_Confirm))
# 正式 @522dmnec
# 開發 @268tfltr
ButtonsTemplateJsonString_ShareProfile = """
{
  "type": "template",
  "altText": "this is a confirm template",
  "template": {
    "type": "confirm",
    "actions": [
      {
        "type": "uri",
        "label": "現在分享",
        "uri": "line://nv/recommendOA/@522dmnec"
      },
      {
        "type": "message",
        "label": "下次再說",
        "text": "^_^"
      }
    ],
    "text": "分享去"
  }
}
"""
ButtonsTemplate_ShareProfile = TemplateSendMessage.new_from_json_dict(json.loads(ButtonsTemplateJsonString_ShareProfile))

ButtonsTemplateJsonString_ShareID = """
{
  "type": "template",
  "altText": "this is a confirm template",
  "template": {
    "type": "confirm",
    "actions": [
      {
        "type": "uri",
        "label": "現在分享",
        "uri": "line://msg/text/?歡迎加入[路見不平]好友:@522dmnec"
      },
      {
        "type": "message",
        "label": "下次再說",
        "text": "^_^"
      }
    ],
    "text": "分享去"
  }
}
"""
ButtonsTemplate_ShareID = TemplateSendMessage.new_from_json_dict(json.loads(ButtonsTemplateJsonString_ShareID))

Quickreply_Friend = TextSendMessage(
    text='如果你喜歡本服務，歡迎分享',
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=PostbackAction(label="分享Line好友資料", data="ShareProfile")
            ),
            QuickReplyButton(
                action=PostbackAction(label="分享Line ID", data="ShareID")
            ),
            QuickReplyButton(
                action=PostbackAction(label="分享Line QR code", data="ShareQR")
            ),
        ]
    )
)
# In[ ]:

# 告知handler，如果收到FollowEvent，則做下面的方法處理
# handler如果收到關注事件時，執行下面的方法
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)

    # 將用戶資訊存在檔案內
    my_database.csv_record_user_info(json.dumps(vars(user_profile), sort_keys=True))

    # 將菜單綁定在用戶身上
    linkRichMenuId = secretFileContentJson.get("rich_menu_id")
    # linkResult = line_bot_api.link_rich_menu_to_user(secretFileContentJson["self_user_id"], linkRichMenuId)
    linkResult = line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)

    # 回覆文字消息與圖片消息
    import random
    sample_img = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 2)
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text="歡迎加入通報道路坑洞的行動"),
            TextSendMessage(text="讓我們一起路見不平通報坑洞"),
            TextSendMessage(text="測試圖: (輸入 '測試' 提供其他測試圖)"),
            ImageSendMessage(original_content_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg',
                             preview_image_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg')
        ]
    )

# In[ ]:

def local_mode(dict_to_file):
    id = 0
    # 將資訊存到 PostgreSQL
    id = my_database.database_insert_data(dict_to_file['line_name'],
                                          dict_to_file['user_id'],
                                          dict_to_file['address'],
                                          dict_to_file['latitude'],
                                          dict_to_file['longitude'],
                                          dict_to_file['image_name'],
                                          dict_to_file['date'])

    # 將圖片存到 PostgreSQL
    my_database.database_update_img_byte('img_byte_ori', dict_to_file['image_name'], id)

    # 模型檢測
    path = dict_to_file['image_name']
    pred = dict_to_file['image_name'].replace('ori', 'pred')
    detect.pred_image('./images/' + path, './images/' + pred)

    # 將結果檔名寫入 PostgreSQL
    my_database.database_update_img_pred_name(dict_to_file['image_name'], pred)

    # 將圖片存到 PostgreSQL
    my_database.database_update_img_byte('img_byte_pred', pred, id)

    return id

def depoly_mode(dict_to_file):
    # 將資訊存到 PostgreSQL
    id = my_database.database_insert_data(dict_to_file['line_name'],
                                          dict_to_file['user_id'],
                                          dict_to_file['address'],
                                          dict_to_file['latitude'],
                                          dict_to_file['longitude'],
                                          dict_to_file['image_name'],
                                          dict_to_file['date'])

    # 將圖片存到 PostgreSQL
    my_database.database_update_img_byte('img_byte_ori', dict_to_file['image_name'], id)

    # 將圖片上傳到S3
    my_database.s3_upload('./images/' + dict_to_file['image_name'], dict_to_file['image_name'])

    # 上傳圖片至 S3 的時候會觸發 lambda 執行模型檢測
    # 需等待其完成並將檢測後圖片上傳 S3 以及填寫 postgresql

    # 持續偵測 PostgreSQL 內是否有檔名
    pred = dict_to_file['image_name'].replace('ori', 'pred')
    done = 0
    for i in range(0, 30):
        img_name_pred = my_database.database_query_pred_img(id)
        if img_name_pred[0][0] == None:
            print(dict_to_file['line_name'], '尚未取得結果')
            time.sleep(1)
        else:
            print(dict_to_file['line_name'], '取得結果:', img_name_pred[0][0])
            done = 1
            break
    if done == 1:
        # 將檢測完圖片從S3下載
        my_database.s3_downloadd(pred, './images/' + pred)
        # 將圖片存到 PostgreSQL
        my_database.database_update_img_byte('img_byte_pred', pred, id)
    else:
        pass

    return id

# In[ ]:
'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    import random
    sample_img = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 2)
    if '測試' == event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg',
                             preview_image_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg')
        )
        return 'OK'
    if '查詢' in event.message.text[0:2]:
        if len(event.message.text) > 2:
            id = int(event.message.text[2:])
            query_text = my_database.database_query_info(id)
            img_name_pred = my_database.database_download_img_byte(id)
            if query_text == '查無資料':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=query_text)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text=query_text),
                        ImageSendMessage(
                            original_content_url='https://%s/images/' % server_url + img_name_pred,
                            preview_image_url='https://%s/images/' % server_url + img_name_pred)
                    ]
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='缺少回報編號')
            )
            return 'OK'
    if '[bot]' not in event.message.text:
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=f'回聲測試: {event.message.text}')
        # )
        return 'OK'

    user_id_exist = 0
    dict_to_file = {}
    for d in collect_report:
        if d['user_id'] == event.source.user_id:
            user_id_exist = 1
            dict_to_file = d
            break

    if event.message.text.find('[bot]確認回報') == 0:
        if user_id_exist == 1:
            if 'reporting' in dict_to_file.keys():
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='正在處理中...請稍後')
                )
                return 'OK'
            else:
                dict_to_file['reporting'] = 1

            # 將資訊存在檔案內
            my_database.csv_record_report_info(dict_to_file['line_name'], dict_to_file['user_id'],
                                               dict_to_file['address'], dict_to_file['latitude'],
                                               dict_to_file['longitude'], dict_to_file['image_name'],
                                               dict_to_file['date'])
            print(collect_report, '紀錄到csv')


            # 選擇模型部屬方式
            if SET_DEPOLY_MODE == 'local':
                id = local_mode(dict_to_file)
            else:
                id = depoly_mode(dict_to_file)

            pred = dict_to_file['image_name'].replace('ori', 'pred')
            collect_report.remove(dict_to_file)

            # 回覆文字消息與圖片消息
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=f'回報編號: {id}'),
                    TextSendMessage(text='結果:'),
                    ImageSendMessage(original_content_url='https://%s/images/' % server_url + pred,
                                     preview_image_url='https://%s/images/' % server_url + pred),

                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Oops...出了點小問題，請重新點擊坑洞通報')
            )

    if event.message.text.find('[bot]放棄回報') == 0:
        if user_id_exist == 1:
            if 'reporting' in dict_to_file.keys():
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='已進入回報流程...無須取消')
                )
                return 'OK'
            else:
                collect_report.remove(dict_to_file)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='已放棄此筆回報')
                )
        else:
            pass

# In[ ]:
'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    user_id_exist = 0
    dict_to_file = {}
    for d in collect_report:
        if d['user_id'] == event.source.user_id:
            user_id_exist = 1
            dict_to_file = d # 注意: 這邊使用 dict_to_file = d, 因此對 dict_to_file 的修改都會同步修改 collect_report
            break

    if user_id_exist == 1:
        # 以時間為檔名來命名使用者上傳的圖片
        date = dict_to_file['date'].replace('-', '', 2).replace(' ', '', 1).replace(':', '', 2)
        image_name = event.source.user_id + '_' + date + '_ori.jpg'
        dict_to_file['image_name'] = image_name
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Oops...出了點小問題，請重新點擊坑洞通報')
        )
        return 'OK'

    # 使用 message id 去跟 line 取回使用者上傳的圖片
    message_content = line_bot_api.get_message_content(event.message.id)

    # 將圖片存檔
    with open('./images/'+dict_to_file['image_name'], 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # 將圖片上傳到S3
    # my_database.s3_upload('./images/' + dict_to_file['image_name'], dict_to_file['image_name'])

    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text='Image has Upload' + ' ' + event.message.id),
            TextSendMessage(text='請繼續上傳位置'),
            ButtonsTemplate_Location
        ]
    )

# In[ ]:

# 用戶點擊傳送位置，觸發LocationMessage，對其回傳做相對應處理
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    line_name = vars(user_profile)["display_name"]
    user_id = vars(user_profile)["user_id"]
    # 取出消息內的位置資料
    address = event.message.address
    latitude = event.message.latitude
    longitude = event.message.longitude

    user_id_exist = 0
    dict_to_file = {}
    for d in collect_report:
        if d['user_id'] == user_id:
            user_id_exist = 1
            dict_to_file = d
            break
    if user_id_exist == 1:
        dict_to_file['address'] = address
        dict_to_file['latitude'] = latitude
        dict_to_file['longitude'] = longitude
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Oops...出了點小問題，請重新點擊坑洞通報')
        )
        return 'OK'

    # 檢查是否已經上完成上傳照片
    if 'image_name' not in dict_to_file.keys():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Oops......出了點小問題，請重新點擊坑洞通報')
        )
        return 'OK'

    # 資訊收集完成
    if len(dict_to_file) == 7:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text='Location has Upload' + ' ' + event.message.address),
                ButtonsTemplate_Confirm
            ]
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Oops....出了點小問題，請重新點擊坑洞通報')
        )

# In[ ]:

import random
@handler.add(PostbackEvent)
def handle_post_message(event):
    print(event.source.user_id, '點 PostbackEvent', event.postback.data)

    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    line_name = vars(user_profile)["display_name"]
    user_id = vars(user_profile)["user_id"]

    # 目前時間
    tw_tz = pytz.timezone('Asia/Taipei')
    localtime = datetime.datetime.now(tz=tw_tz)
    # 轉換成文字格式
    localtime_to_file = (localtime.strftime("%Y-%m-%d %H:%M:%S"))

    if (event.postback.data.find('[bot]坑洞通報') == 0):
        user_id_exist = 0
        for d in collect_report:
            if d['user_id'] == user_id:
                user_id_exist = 1
                break
        if user_id_exist == 0:
            collect_report.append({})
            collect_report[-1]['user_id'] = user_id
            collect_report[-1]['line_name'] = line_name
            collect_report[-1]['date'] = localtime_to_file

        if SET_DEPOLY_MODE == 'local':
            pass
        else:
            try:
                requests.get('https://hm61ggtpm7.execute-api.ap-northeast-1.amazonaws.com/default/lambda_function',timeout=0.5)
            except:
                pass

        line_bot_api.reply_message(
            event.reply_token,
            ButtonsTemplate_Image)

    if (event.postback.data.find('[bot]查詢') == 0):
        query_text = my_database.database_query_id_by_user(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=query_text),
                TextSendMessage(text='輸入 [查詢+回報編號] 進行查詢'),
                TextSendMessage(text='例如: 查詢12')
            ]
        )

    if (event.postback.data.find('[bot]分享') == 0):
        line_bot_api.reply_message(
            event.reply_token,
            Quickreply_Friend
        )

    if (event.postback.data.find('[bot]網頁') == 0):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='尚未實現')
        )

    if (event.postback.data.find('[bot]測試') == 0):
        sample_img = random.sample([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 5)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg',
                             preview_image_url='https://%s/demo_images/' % server_url + str(sample_img[0]) + '.jpg')
        )

    if (event.postback.data.find('ShareProfile') == 0):
        line_bot_api.reply_message(
            event.reply_token,
            ButtonsTemplate_ShareProfile
        )

    if (event.postback.data.find('ShareID') == 0):
        line_bot_api.reply_message(
            event.reply_token,
            ButtonsTemplate_ShareID
        )

    if (event.postback.data.find('ShareQR') == 0):
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(original_content_url='https://%s/QRcode/LINEQRcode.jpg' % server_url,
                                 preview_image_url='https://%s/QRcode/LINEQRcode.jpg' % server_url),
                TextMessage(text='點擊圖片右邊分享圖示')
            ]
        )


# In[ ]:



collect_report = []



# 使用debug
@app.route("/debug", methods=['GET'])
def check_files():
    print('list ./:', os.listdir('./'))
    print('users.txt')
    f = open('./users.txt', 'r')
    data = f.readlines()
    for d in data:
        print(d)
    f.close()

    print('user_report.csv')
    f = open('./user_report.csv', 'r')
    data = f.readlines()
    for d in data:
        print(d)
    f.close()

    print('images/')
    print(os.listdir('./images/'))

    return 'OK'

# from keras.models import load_model
# import numpy as np
# # 使用dltest
# @app.route("/dltest", methods=['GET'])
# def dltest():
#     # 載入模型
#     print('載入模型')
#     model_load = load_model('model.h5')
#     # 讀取
#     print('讀取')
#     test = np.load('x_test.npy')
#     # input前處理
#     print('前處理')
#     test = test / 255
#     test = test.reshape(1, 28, 28, 1)
#     print('預測')
#     pred = model_load.predict_classes(test)
#     print(pred)
#     return 'dl test OK'

# In[ ]:

print('init start ----->')

if my_database.database_init() == True:
    print('PostgreSQL status OK')
else:
    print('PostgreSQL status not OK')

# if my_database.s3_init() == True:
#     print('s3 status OK')
# else:
#     print('s3 status not OK')

if my_database.csv_init() == True:
    print('local csv status OK')
else:
    print('local csv status not OK')

if my_database.images_init() == True:
    print('local images folder status OK')
else:
    print('local images folder status not OK')

print('<---- init end>')

# In[ ]:


#  '''

#  執行此句，啟動Server，觀察後，按左上方塊，停用Server

#  '''

if SET_DEPOLY_MODE == 'local':
    if __name__ == "__main__":
        app.run(host='0.0.0.0')


# In[ ]:


#  '''

#  Application 運行（heroku版）

#  '''

if SET_DEPOLY_MODE == 'depoly':
    import os
    if __name__ == "__main__":
        app.run(host='0.0.0.0',port=os.environ['PORT'])
