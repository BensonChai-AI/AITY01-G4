from flask import Flask
from flask import render_template, send_from_directory
import psycopg2
import json
import datetime

app = Flask(__name__,static_url_path="/",static_folder="./")
# flask網頁框架起點
app.send_file_max_age_default = datetime.timedelta(seconds=30)
#設定網頁30秒就會清除緩存，這樣30秒後重新整理才能重跑整個flask重跑資料內容刷新網頁

def renew_json() :
    # 以下是建立資料庫連線並創建json

    # conn = psycopg2.connect(database="d1ii52tsb31ga5",
    #                         user="vgnorlhadkiiiv",
    #                         password="094ca31076b8fcbc09cab98046608aba4bfec2f12ef8bc41c1effcc1937ddf1f",
    #                         host="ec2-3-234-109-123.compute-1.amazonaws.com",
    #                         port="5432")
    conn = psycopg2.connect(database="資料庫名稱",
                            user="使用者名稱",
                            password="資料庫密碼",
                            host="資料庫位址",
                            port="接口")
    cur = conn.cursor()
    cur.execute("SELECT * FROM project_data order by id")
    #從table名為project_data的資料表以id為排序拿出所有資料

    rows = cur.fetchall()    # all rows in table
    # 以上是抓取資料庫所有資料

    d1 = {"a": []}
    for i in rows:
        if i[7] == None:
            pass
        else:
            d2 = {"id": int(i[0]), "address": str(i[3].rstrip()), "lat": float(i[4]), "lng": float(i[5]),
                  "time": str(str(i[8])), "pre_name": str(i[7].rstrip())}
            d1["a"].append(d2)
    with open('./json_files/test.json', 'w', encoding='utf-8') as f:
        json.dump(d1, f, ensure_ascii=False, indent=1)
    # 以上是創立google map api 標記所需的json檔放至json_files

    for i in rows:
        if i[7] != None:
            f = open(("./road_images/" + i[7]).rstrip(), 'wb')
            f.write(i[11])
        else:
            pass
    #建立所有已預測的圖片檔(用二進制碼)至road_images

    conn.commit()
    cur.close()
    conn.close()
    # 到此關閉資料庫連結，建立完json、與圖片檔

renew_json()
#跑 renew_json

@app.route('/')
def show_html():
    return render_template('./index.html')
# 主頁面顯示html檔
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)
# 在主頁面讀取assests資料夾裡的所有檔案
@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)
# 在主頁面讀取images資料夾裡的所有檔案
@app.route('/json_files/<path:path>')
def send_json(path):
    return send_from_directory('json_files', path)
# 在主頁面讀取json_files資料夾裡的所有檔案
@app.route('/road_images/<path:path>')
def send_road(path):
    return send_from_directory('road_images', path)
# 在主頁面讀取road_images資料夾裡的所有檔案

#####
# @app.route('/debug')
# def debug():
#     print(glob.glob('./road_images/*'))
# 看偵錯報告時需開啟
#####

if __name__ == '__main__':
    app.run(debug=True)
# 跑這個flask



