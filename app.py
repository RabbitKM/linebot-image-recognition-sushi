#------------------------------------載入套件--------------------------------------#
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, ImageMessage
)

from google.cloud import storage
from google.cloud import firestore

import time

# 圖片下載與上傳專用
import urllib.request
import os

# 建立日誌紀錄設定檔
#https://googleapis.dev/python/logging/latest/stdlib-usage.html
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

#------------------------------------環境設定---------------------------------------#
# 啟用log的客戶端
client = google.cloud.logging.Client()


# 建立line event log，用來記錄line event
bot_event_handler = CloudLoggingHandler(client,name="cxcxc_bot_event")
bot_event_logger=logging.getLogger('cxcxc_bot_event')
bot_event_logger.setLevel(logging.INFO)
bot_event_logger.addHandler(bot_event_handler)

app = Flask(__name__)
# 註冊機器人
line_bot_api = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
handler = os.environ["LINE_CHANNEL_SECRET"]
bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']

# 設定機器人訪問入口
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    # 消息整個交給bot_event_logger，請它傳回GCP
    bot_event_logger.info(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
#------------------------------------全域變數---------------------------------------#
# # 紀錄劇情總次數
# opener_1 = 0
# opener_2 = 0
# opener_3 = 0
# opener_4 = 0
# plot1_1 = 0
# plot1_2 = 0
# plot2_1 = 0
# plot2_2 = 0
# plot3_1 = 0
# plot3_2 = 0
# score_1 = 0
# score_2 = 0
# ff_1 = 0
# ff_2 = 0
# ff_3 = 0
# ff_4 = 0

# # 存放各劇情百分比
# opener_1_perc = None
# opener_2_perc = None
# opener_3_perc = None
# opener_4_perc = None
# plot1_1_perc = None
# plot1_2_perc = None
# plot2_1_perc = None
# plot2_2_perc = None
# plot3_1_perc = None
# plot3_2_perc = None
# score_1_perc = None
# score_2_perc = None
# ff_1_perc = None
# ff_2_perc = None
# ff_3_perc = None
# ff_4_perc = None
#------------------------------------回傳圖片設定區---------------------------------------#
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# analyze_truth_image_message=ImageSendMessage(
#       original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/0260da9db3d307b8d575033d26c954ba.png',
#       preview_image_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/0260da9db3d307b8d575033d26c954ba.png'
#       )

# 紀錄圖片辨識劇情階段
# record = 0

#------------------------------------氣泡訊息設定區---------------------------------------#
# 引入相關套件
from linebot.models import (
    MessageAction, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    QuickReply, QuickReplyButton
)

# QRB1: 滿意度調查
QRB1_PB1 = QuickReplyButton(
    image_url='https://1.bp.blogspot.com/-hfUIDwwrnBI/VWmA9NFiw1I/AAAAAAAAt2Y/cIm432inuZU/s800/mark_manpu07_heart.png',
    action=PostbackAction(label='很有趣',text='@很有趣', data='QRB1-1')
)
QRB1_PB2 = QuickReplyButton(
    image_url='https://3.bp.blogspot.com/-nVaIqmTAb_w/VWmBBFZU5jI/AAAAAAAAt3o/G8HOQjh4lpU/s800/mark_manpu15_shock.png',
    action=PostbackAction(label='還好',text='@還好', data='QRB1-2')
)

# QRB1的List
QRB1_list = QuickReply(
    items = [QRB1_PB1, QRB1_PB2]
)

# QRB2: 壽司喜好調查
QRB2_PB1 = QuickReplyButton(
    image_url='https://4.bp.blogspot.com/-hmdGf6or_BE/VGLLW45uf_I/AAAAAAAAoxk/TC5H4euUlTc/s800/sushi_harasu.png',
    action=PostbackAction(label='鮭魚壽司',text='@鮭魚壽司', data='QRB2-1')
)
QRB2_PB2 = QuickReplyButton(
    image_url='https://2.bp.blogspot.com/-h1_jBlYNEVE/USyJ2MA1-3I/AAAAAAAAOb8/eWYDN_SJVbk/s1600/sushi_chutoro.png',
    action=PostbackAction(label='鮪魚壽司',text='@鮪魚壽司', data='QRB2-2')
)
QRB2_PB3 = QuickReplyButton(
    image_url='https://2.bp.blogspot.com/-LOjIxa99eko/Wp93wRvqa9I/AAAAAAABKoM/NOpHrcAZItgx-QOoZwPF-UYI64F1LuzKgCLcBGAs/s800/food_inarizushi_one.png',
    action=PostbackAction(label='豆皮壽司',text='@豆皮壽司', data='QRB2-3')
)
QRB2_PB4 = QuickReplyButton(
    image_url='https://2.bp.blogspot.com/--yCZ9NOGK0Q/W1a5NUMb33I/AAAAAAABNko/KdbkLvHkltYeMpCG-TWtmStiAbT1p-MCACLcBGAs/s800/sushi_oke_nigiri.png',
    action=PostbackAction(label='其他',text='@其他', data='QRB2-4')
)

# QRB2的List
QRB2_list = QuickReply(
    items = [QRB2_PB1, QRB2_PB2, QRB2_PB3, QRB2_PB4]
)


# QRB3: 我還要看更多！！ (看其他統計表)
QRB3_PB1 = QuickReplyButton(
    image_url='https://i.imgur.com/OZc2klw.png',
    action=PostbackAction(label='我還要看更多！！',text='@我還要看更多！！', data='QRB3-1')
)

# QRB3的List
QRB3_list = QuickReply(
    items = [QRB3_PB1]
)


#------------------------------------彈性訊息設定區---------------------------------------#
# 第一個範例
from linebot.models import FlexSendMessage
from linebot.models.flex_message import (
    BubbleContainer, ImageComponent
)
from linebot.models.actions import URIAction

# fm1: 滿意度調查
fm1_m = FlexSendMessage(
    alt_text='滿意度調查',
    contents={
        "type": "bubble",
        "direction": "ltr",
        "hero": {
            "type": "image",
            "url": "https://i.imgur.com/oc5Uy9H.png",
            "size": "full",
            "aspectRatio": "2:1.5",
            "backgroundColor": "#59B2CB"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "Body",
                "align": "center",
                "contents": [
                {
                    "type": "span",
                    "text": "對這次的故事還滿意嗎？",
                    "size": "lg",
                    "color": "#28758AFF",
                    "weight": "bold"
                }
                ]
            }
            ]
        }
    },
    quick_reply = QRB1_list
)

# fm2: 壽司喜好調查
fm2_m = FlexSendMessage(
    alt_text='壽司喜好調查',
    contents={
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "Reply",
                "align": "center",
                "contents": []
            }
            ]
        },
        "hero": {
            "type": "image",
            "url": "https://3.bp.blogspot.com/-imoetF1R6G4/W3aa_LjAGnI/AAAAAAABN9c/gFgRVNVJb40o5Wl-Yyv3niNvAAdrjrFLACLcBGAs/s800/bg_kaitenzushi.jpg",
            "size": "full",
            "aspectRatio": "1.51:1",
            "aspectMode": "fit"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": " What would you like to eat first?",
                "align": "center",
                "contents": []
            }
            ]
        }
    },
    quick_reply = QRB2_list
)

# fm3: 壽司喜好統計表
def flex_out_fm3(ff_1_perc, ff_2_perc, ff_3_perc, ff_4_perc, favorite_food_total, total_people):
    fm3_m = FlexSendMessage(
        alt_text='壽司喜好統計表',
        contents={
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "flex": 0,
                "backgroundColor": "#000000FF",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "大家の小祕密💗  ",
                        "weight": "bold",
                        "size": "xxl",
                        "color": "#FFFFFFFF",
                        "align": "start",
                    }
                    ]
                }
                ]
            },
            "hero": {
                "type": "image",
                "url": "https://x.nctu.app/img/akw2.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://linecorp.com"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                "type": "uri",
                "uri": "https://linecorp.com"
                },
                "backgroundColor": "#000000FF",
                "contents": [
                {
                    "type": "text",
                    "text": "讓我看看!!",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#FFFFFFFF",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://4.bp.blogspot.com/-hmdGf6or_BE/VGLLW45uf_I/AAAAAAAAoxk/TC5H4euUlTc/s800/sushi_harasu.png"
                        },
                        {
                            "type": "text",
                            "text": "鮭魚壽司",
                            "weight": "bold",
                            "color": "#FFFFFFFF",
                            "margin": "sm",
                        },
                        {
                            "type": "text",
                            "text": ff_1_perc,
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://2.bp.blogspot.com/-h1_jBlYNEVE/USyJ2MA1-3I/AAAAAAAAOb8/eWYDN_SJVbk/s1600/sushi_chutoro.png"
                        },
                        {
                            "type": "text",
                            "text": "鮪魚壽司",
                            "weight": "bold",
                            "color": "#FFFFFFFF",
                            "flex": 0,
                            "margin": "sm",
                        },
                        {
                            "type": "text",
                            "text": ff_2_perc,
                            "weight": "regular",
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://2.bp.blogspot.com/-LOjIxa99eko/Wp93wRvqa9I/AAAAAAABKoM/NOpHrcAZItgx-QOoZwPF-UYI64F1LuzKgCLcBGAs/s800/food_inarizushi_one.png"
                        },
                        {
                            "type": "text",
                            "text": "豆皮壽司",
                            "weight": "bold",
                            "color": "#FFFFFFFF",
                            "margin": "sm",
                        },
                        {
                            "type": "text",
                            "text": ff_3_perc,
                            "weight": "regular",
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "icon",
                            "url": "https://2.bp.blogspot.com/--yCZ9NOGK0Q/W1a5NUMb33I/AAAAAAABNko/KdbkLvHkltYeMpCG-TWtmStiAbT1p-MCACLcBGAs/s800/sushi_oke_nigiri.png"
                        },
                        {
                            "type": "text",
                            "text": "其他",
                            "weight": "bold",
                            "color": "#FFFFFFFF",
                            "margin": "sm",
                        },
                        {
                            "type": "text",
                            "text": ff_4_perc,
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "以上結果來自"+str(total_people)+"位阿瑋點擊統計",
                    "size": "sm",
                    "color": "#7BA46EFF",
                },
                {
                    "type": "text",
                    "text": "點擊次數"+str(favorite_food_total),
                    "size": "sm",
                    "color": "#AAAAAA",
                }

                ]
            },
        },
        quick_reply = QRB3_list
    )
    return fm3_m

def Flex_out_fm_mix(total_people, opener_total, plot1_total, plot2_total, plot3_total, opener_1_perc, opener_2_perc, opener_3_perc, opener_4_perc, plot1_1_perc, plot1_2_perc, plot2_1_perc, plot2_2_perc, plot3_1_perc, plot3_2_perc):
    contents1 = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "contents": [
        {
            "type": "text",
            "text": "大家下班都怎麼Chill?",
            "weight": "bold",
            "size": "xl",
        }
        ]
    },
    "hero": {
        "type": "image",
        "url": "https://images2.gamme.com.tw/news2/2018/15/98/qZqTnZ6Vlp_VqaQ.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://3.bp.blogspot.com/-rPTPV8qyqc8/W5IAR6v75iI/AAAAAAABOzY/ByMcMGbiLOkZILU1za4AVCyXwdP_-CC7ACLcBGAs/s800/yopparai_businessman.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "喝一杯",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": opener_1_perc,
                    "size": "xl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://1.bp.blogspot.com/-mkyd8jegvkw/Vmfqjvne_YI/AAAAAAAA1mM/6LimCRu1mhs/s800/kitaku_hitori.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "回家",
                    "weight": "bold",
                    "size": "xxl",
                    "flex": 0,
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": opener_2_perc,
                    "size": "xl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://4.bp.blogspot.com/-sFjkZhZrb1M/VOsKCU-JByI/AAAAAAAArw8/DvMpA1LFfnI/s800/sushi_counter.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "吃好料",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": opener_3_perc,
                    "size": "xl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://1.bp.blogspot.com/-IBEo3d-WLTw/XMZ-AlmUbjI/AAAAAAABSnM/y3F2RNhfgYAAPuL2Aii-wQK2jQswt8itwCLcBGAs/s800/seisyun_hamabe_oikakekko_couple.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "放閃",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": "死ね",
                    "size": "xxs",
                    "color": "#E3DFDFFF",
                    "align": "start",
                    "margin": "none",
                    "decoration": "line-through",
                },
                {
                    "type": "text",
                    "text": opener_4_perc,
                    "size": "xl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            }
            ]
        },
        {
            "type": "text",
            "text": "我是個成熟的大人了，我全都要",
            "size": "md",
            "color": "#9A9A9AFF",
            "wrap": True,
        }
        ]
    },
    }

    contents2 = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "contents": [
        {
            "type": "text",
            "text": "救命...",
            "weight": "bold",
            "size": "xl",
        }
        ]
    },
    "hero": {
        "type": "image",
        "url": "https://img.league-funny.com/imgur/164950684761_n.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://2.bp.blogspot.com/-WZDpwP1Zg0c/UZ2VEErPIaI/AAAAAAAATtw/Rqs2PaN-xJ0/s800/kyosyu_boy.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "打招呼",
                    "weight": "bold",
                    "size": "3xl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot1_1_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://2.bp.blogspot.com/-1gAgQDz_sjo/WIHlM6wqyJI/AAAAAAABBNk/EIfeOJT7fwc4xGYim4KYxqtJGJFxWj8bgCLcB/s800/ninja_tenjo.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "潛行!!",
                    "weight": "bold",
                    "size": "3xl",
                    "flex": 0,
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot1_2_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            }
            ]
        },
        {
            "type": "text",
            "text": "以上結果來自"+str(total_people)+"位褪色者點擊統計",
            "size": "md",
            "color": "#888C3EFF",
            "wrap": True,
        },
        {
            "type": "text",
            "text": "點擊次數"+str(plot1_total),
            "color": "#AAAAAA",
        }
        ]
    },
    }

    contents3 = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "contents": [
        {
            "type": "text",
            "text": "!",
            "weight": "bold",
            "size": "xl",
        }
        ]
    },
    "hero": {
        "type": "image",
        "url": "https://www.pokemon.co.jp/ex/bdsp/assets/img/news/tc/img_news_14.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://4.bp.blogspot.com/-gU1F5gSME8w/WdyDK2KmIjI/AAAAAAABHaA/Up8EMGa0uK4yZGI6QF8TFPZmgrAJkTgRACLcBGAs/s800/baseball_shinpan_safe.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "觀望",
                    "weight": "bold",
                    "size": "3xl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot2_1_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://3.bp.blogspot.com/-UIoC4WJrWdk/UpGGw9EspqI/AAAAAAAAa_U/lwvynKIXyfM/s800/fishing_boy.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "奮力一搏",
                    "weight": "bold",
                    "size": "3xl",
                    "flex": 0,
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot2_2_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            }
            ]
        },
        {
            "type": "text",
            "text": "以上結果來自"+str(total_people)+"位靠黑鮪魚賺大錢的人點擊統計",
            "size": "md",
            "color": "#980000FF",
            "wrap": True,
        },
        {
            "type": "text",
            "text": "點擊次數"+str(plot2_total),
            "color": "#AAAAAA",
        }
        ]
    },
    }

    contents4 ={
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "flex": 0,
        "contents": [
        {
            "type": "text",
            "text": "米勾~",
            "weight": "bold",
            "size": "xl",
        }
        ]
    },
    "hero": {
        "type": "image",
        "url": "https://cdn.hk01.com/di/media/images/589043/org/a3285982f2bb68f5061d52002e558344.JPG/Y_JvbKeCUdKnfJheBLW4_grjFKbYKMI65xgSbOcYEmw?v=w1920",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "action": {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://1.bp.blogspot.com/-h8TobvWuywc/VCkbOwPJPNI/AAAAAAAAnDg/5H6ARSopjWk/s800/omatsuri_awaodori.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "What...",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot3_1_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://1.bp.blogspot.com/-gSjMiM-eGz4/WFJWTT8DHXI/AAAAAAABAaY/cY1jdUf9AfsHKMSclNfB7FwkUVjF1VSFgCLcB/s800/syugyou_goma_gyou.png",
                    "size": "3xl"
                },
                {
                    "type": "text",
                    "text": "供奉",
                    "weight": "bold",
                    "size": "3xl",
                    "flex": 0,
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": plot3_2_perc,
                    "size": "xxl",
                    "color": "#AAAAAA",
                    "align": "end",
                }
                ]
            }
            ]
        },
        {
            "type": "text",
            "text": "以上結果來自"+str(total_people)+"位國民老婆の老公點擊統計",
            "size": "md",
            "color": "#403394FF",
            "wrap": True,
        },
        {
            "type": "text",
            "text": "點擊次數"+str(plot3_total),
            "color": "#AAAAAA",
        }
        ]
    },
    }

    # 合併全部統計表
    fm_mix = FlexSendMessage(
        alt_text='我還要看更多！！',
        contents={
            "type": "carousel",
            "contents": [contents1, contents2, contents3, contents4]
        }
    )

    return fm_mix
#------------------------------------範本訊息設定區---------------------------------------#
# 引入所需要的消息與模板消息
from linebot.models import (
    MessageEvent, TemplateSendMessage , PostbackEvent
)
# 引入按鍵模板
from linebot.models.template import(
    ButtonsTemplate, ConfirmTemplate
)

# bt1: 下班要做什麼
bt1_m = TemplateSendMessage(
    alt_text='下班做點什麼吧',
    template=ButtonsTemplate(
        thumbnail_image_url="https://4.bp.blogspot.com/-58WXqiFyiro/VxC3YLEHP2I/AAAAAAAA548/U-oHhYKu7b8Z2gdv9uys1yy8UN0RTjALQCLcB/s800/businessman_cry_woman.png",
        image_aspect_ratio="square",
        image_size="contain",
        image_background_color="#C95D30",
        title="下班好鬱悶",
        text="做點什麼吧",
        actions=[
          {
            "type": "postback",
            "label": "去酒吧喝一杯",
            "text": "可是沒有錢",
            "data": "BT1-1"
          },
          {
            "type": "postback",
            "label": "別多想了，回家吧",
            "text": "：少年(女)阿！要胸懷大志阿！",
            "data": "BT1-2"
          },
          {
            "type": "postback",
            "label": "去吃點好吃的吧",
            "text": "前有不得了的事物",
            "data": "BT1-3"
          },
          {
            "type": "postback",
            "label": "去找另一伴聊聊",
            "text": "：睡吧，睡吧，夢裡什麼都有。",
            "data": "BT1-4"
          }
        ],
  )
)

# bt2: 劇情1 - 巨熊補鮭魚
bt2_m = TemplateSendMessage(
    alt_text='前有巨熊',
    template=ButtonsTemplate(
        thumbnail_image_url="https://4.bp.blogspot.com/--ysNcYpsGXU/V9vB__9_KwI/AAAAAAAA96s/VWdgwqiOfzcahqy5VK_FisOqFHwo2os4gCLcB/s800/animal_bear_character.png",
        image_aspect_ratio="square",
        image_size="contain",
        image_background_color="#59B2CB",
        title="前有巨熊",
        text="怎麼辦",
        actions=[
          {
            "type": "postback",
            "label": "上前打聲招呼尋求幫助",
            "text": "Hey Bear!",
            "data": "BT2-1"
          },
          {
            "type": "postback",
            "label": "壓低身子躲進旁邊的草叢中",
            "text": "(我躲)",
            "data": "BT2-2"
          },
        ],
  )
)

# bt3: 劇情1 - 猜鮭魚
bt3_m = TemplateSendMessage(
    alt_text='棕熊喜歡什麼呢',
    template=ButtonsTemplate(
        thumbnail_image_url="https://i.imgur.com/WA0raCc.png",
        image_size="contain",
        image_background_color="#152346",
        title="棕熊喜愛的魚類",
        text="猜一種握壽司",
        actions=[
          {
            "type": "uri",
            "label": "上傳照片",
            "uri": "https://line.me/R/nv/cameraRoll/single"
          },
        ],
  )
)

# bt4: 劇情2 - 釣起黑鮪魚
bt4_m = TemplateSendMessage(
    alt_text='力魯嘶吼中',
    template=ConfirmTemplate(
        text="突然間手中的力魯發出了嘶吼， 你心想一定要做點甚麼：",
        actions=[
            {
                "type": "postback",
                "label": "觀望看看",
                "text": "猶豫，就會敗北。",
                "data": "BT4-1"
            },
            {
                "type": "postback",
                "label": "奮力一搏",
                "text": "喝啊～～～",
                "data": "BT4-2"
            }
    ],
  )
)

# bt5: 劇情2 - 猜鮪魚
bt5_m = TemplateSendMessage(
    alt_text='船長朝思暮想的是?',
    template=ButtonsTemplate(
        thumbnail_image_url="https://i.imgur.com/WA0raCc.png",
        image_size="contain",
        image_background_color="#152346",
        title="船長朝思暮想的究竟是!?",
        text="猜一種握壽司",
        actions=[
          {
            "type": "uri",
            "label": "上傳照片",
            "uri": "https://line.me/R/nv/cameraRoll/single"
          },
        ],
  )
)

# bt6: 劇情3 - 狐狸與豆皮
bt6_m = TemplateSendMessage(
    alt_text='命懸一線',
    template=ButtonsTemplate(
        thumbnail_image_url="https://p2.bahamut.com.tw/HOME/creationCover/65/0004637865_B.JPG",
        title="緊張緊張緊張，刺激刺激刺激，命懸一線的你",
        text="必須做點甚麼：",
        actions=[
          {
            "type": "postback",
            "label": "What the fox say？",
            "text": "Ring-ding-ding-ding!",
            "data": "BT6-1"
          },
          {
            "type": "postback",
            "label": "供奉出手上的鮮度君",
            "text": "(這個香味是!)",
            "data": "BT6-2"
          },
        ],
  )
)

# bt7: 劇情3 - 猜豆皮
bt7_m = TemplateSendMessage(
    alt_text='狐狸最喜愛的食物',
    template=ButtonsTemplate(
        thumbnail_image_url="https://i.imgur.com/WA0raCc.png",
        image_size="contain",
        image_background_color="#152346",
        title="相傳狐狸最喜愛的食物",
        text="猜一種壽司",
        actions=[
          {
            "type": "uri",
            "label": "上傳照片",
            "uri": "https://line.me/R/nv/cameraRoll/single"
          },
        ],
    ),
)

#------------------------------------文字訊息設定區---------------------------------------#

#------------------------------------自訂函數設定區---------------------------------------#
def first_user_dict_save(line_user_profile, bucket_name, doc_ref):
    user_dict={
        "user_id":line_user_profile.user_id,
        "picture_url": f"https://storage.googleapis.com/{bucket_name}/destination_blob_name",
        "display_name": line_user_profile.display_name,
        "status_message": line_user_profile.status_message,
        "image_plot": 0,
        "follow_total": 1,
        }
    doc_ref.set(user_dict)
    
    return user_dict

def first_user_event_dict_save(line_user_profile, doc_ref2):
    user_event_dict={
        "user_id": line_user_profile.user_id,
        "display_name": line_user_profile.display_name,
        "status_message": line_user_profile.status_message,
        "opener_1": 0,
        "opener_2": 0,
        "opener_3": 0,
        "opener_4": 0,
        "plot1_1": 0,
        "plot1_2": 0,
        "plot2_1": 0,
        "plot2_2": 0,
        "plot3_1": 0,
        "plot3_2": 0,
        "score_1": 0,
        "score_2": 0,
        "ff_1": 0,
        "ff_2": 0,
        "ff_3": 0,
        "ff_4": 0,
    }
    doc_ref2.set(user_event_dict)
    return user_event_dict

#------------------------------------handler功能區---------------------------------------#
# F01: 關注取用戶資料
@handler.add(FollowEvent)
def handle_follow_event(event):
    # 取個資
    line_user_profile = line_bot_api.get_profile(event.source.user_id)

    # 跟line 取回照片，並放置在本地端
    file_name = line_user_profile.user_id+'.jpg'
    urllib.request.urlretrieve(line_user_profile.picture_url, file_name)

    # 設定內容
    storage_client = storage.Client()
    destination_blob_name=f"{line_user_profile.user_id}/user_pic.png"
    source_file_name=file_name
       
    # 進行上傳
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    # 讀取firestore - 紀錄關注次數
    db = firestore.Client()
    doc_ref = db.collection(u'rb-report-line-user').document(line_user_profile.user_id)
    doc = doc_ref.get()

    # 判斷資料是否存在
    # 存在: image_plot = 0, follow_total + 1.
    # 否則: 新增資料
    if doc.exists:
        user_dict = doc.to_dict()
        user_dict["image_plot"] = 0
        user_dict["follow_total"] += 1
        doc_ref.set(user_dict)    
    else:
        user_dict = first_user_dict_save(line_user_profile, bucket_name, doc_ref)


    # ds2: 事件紀錄
    doc_ref2 = db.collection(u'line-user-event').document(line_user_profile.user_id)
    doc2 = doc_ref2.get()

    # 判斷ds2是否存在
    if doc2.exists:
        pass  
    else:
        first_user_event_dict_save(line_user_profile, doc_ref2)   
    
    # 開場白 (SendMessage最多只能5個)
    line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage('小白是一介平凡的上班族\n化身成小白體驗日常の奇幻冒險\n.\n.\n.'),
        TextSendMessage('「小白阿，你要學會判斷，不要小問題都來問我。」\n\n「有不懂一開始就要問阿，你判斷力真的很有問題。」'),
        TextSendMessage('唉～又來了\n主管老是找我麻煩\n有問題問也不是，不問也不是\n每個月才領25K\n真的快幹不下去了！'),
        TextSendMessage('不管了，先下班再說\n明天還有重要的企劃要處理'),
        bt1_m,
        ]
    )

# F02: 回覆文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取個資
    line_user_profile = line_bot_api.get_profile(event.source.user_id)
    bucket_name = "rabbitkm-0601-user-info"

    # 讀取firestore - 重置圖片劇情用
    db = firestore.Client()
    doc_ref = db.collection(u'rb-report-line-user').document(line_user_profile.user_id)
    doc = doc_ref.get()

    # 判斷資料是否存在
    # 存在: image_plot = 0
    # 否則: 新增資料 (不排除資料庫被清空, 要重建資料.)
    if doc.exists:
        user_dict = doc.to_dict()
    else:
        user_dict = first_user_dict_save(line_user_profile, bucket_name, doc_ref)

    # 需重置劇情對話清單
    reset_list = ['可是沒有錢', '：少年(女)阿！要胸懷大志阿！' , '：睡吧，睡吧，夢裡什麼都有。']

    # 重置劇情
    if event.message.text in reset_list:
        user_dict["image_plot"] = 0
        doc_ref.set(user_dict) 

    # 喜好統計圖關鍵字
    ff_list = ['@鮭魚壽司', '@鮪魚壽司', '@豆皮壽司', '@其他']

#------------------------------------資料庫紀錄按鈕被按了幾次---------------------------------------#
    # 紀錄劇情總次數
    opener_1 = 0
    opener_2 = 0
    opener_3 = 0
    opener_4 = 0
    plot1_1 = 0
    plot1_2 = 0
    plot2_1 = 0
    plot2_2 = 0
    plot3_1 = 0
    plot3_2 = 0
    score_1 = 0
    score_2 = 0
    ff_1 = 0
    ff_2 = 0
    ff_3 = 0
    ff_4 = 0

    # 讀取line-user-event資料
    # 個人
    doc_ref2 = db.collection(u'line-user-event').document(line_user_profile.user_id)
    doc2 = doc_ref2.get()

    # 判斷資料是否存在
    # 存在: 開啟
    # 否則: 新增資料 (不排除資料庫被清空, 要重建資料.)
    if doc2.exists:
        user_event_dict = doc2.to_dict()
    else:
        user_event_dict = first_user_event_dict_save(line_user_profile, doc_ref2)

    # 所有選項字典1 (回應文字: 資料庫欄位名稱)
    ret_dict_all = {
        "可是沒有錢": "opener_1",
        "：少年(女)阿！要胸懷大志阿！": "opener_2",
        "前有不得了的事物": "opener_3",
        "：睡吧，睡吧，夢裡什麼都有。": "opener_4",
        "Hey Bear!": "plot1_1",
        "(我躲)": "plot1_2",
        "猶豫，就會敗北。": "plot2_1",
        "喝啊～～～": "plot2_2",
        "Ring-ding-ding-ding!": "plot3_1",
        "(這個香味是!)": "plot3_2",
        "@很有趣": "score_1",
        "@還好": "score_2",
        "@鮭魚壽司": "ff_1",
        "@鮪魚壽司": "ff_2",
        "@豆皮壽司": "ff_3",
        "@其他": "ff_4",
    }    


    # 若有選到選項: 對應次數+1, 並做所有選項統計
    if event.message.text in ret_dict_all:
        # 個人變數+1後 存到資料表user_event_dict
        user_event_dict[ret_dict_all[event.message.text]] += 1
        doc_ref2.set(user_event_dict)
        
    # 所有人(等個人+完再讀取)
    doc_ref2_all = db.collection(u'line-user-event')
    doc2_all = doc_ref2_all.get()
    
    # 讀取所有人資料後 放入清單中[{},{},{},...]
    doc2_all_list = []
    for doc in doc2_all:
        doc2_all_list.append(doc.to_dict())
    
    # 總人數
    total_people = len(doc2_all_list)

    # 所有劇情按鈕 資料庫欄位名稱 共16個
    ds2_field = {
        "opener_1": opener_1,
        "opener_2": opener_2,
        "opener_3": opener_3,
        "opener_4": opener_4,
        "plot1_1": plot1_1,
        "plot1_2": plot1_2,
        "plot2_1": plot2_1,
        "plot2_2": plot2_2,
        "plot3_1": plot3_1,
        "plot3_2": plot3_2,
        "score_1": score_1,
        "score_2": score_2,
        "ff_1": ff_1,
        "ff_2": ff_2,
        "ff_3": ff_3,
        "ff_4": ff_4,
    }
    # 全部人次數加總後 存入變數
    for dd in doc2_all_list:
        for fd in ds2_field:
            ds2_field[fd] += dd.get(fd)

    # 各種類劇情總點選次數 共6組
    opener_total = ds2_field['opener_1'] + ds2_field['opener_2'] + ds2_field['opener_3'] + ds2_field['opener_4']
    plot1_total = ds2_field['plot1_1'] + ds2_field['plot1_2']
    plot2_total = ds2_field['plot2_1'] + ds2_field['plot2_2']
    plot3_total = ds2_field['plot3_1'] + ds2_field['plot3_2']
    score_total = ds2_field['score_1'] + ds2_field['score_2']
    favorite_food_total = ds2_field['ff_1'] + ds2_field['ff_2'] + ds2_field['ff_3'] + ds2_field['ff_4']


    test1 = [opener_total, plot1_total, plot2_total, plot3_total, score_total, favorite_food_total]    

    # 各選項百分比%
    opener_1_perc = f"{round((ds2_field['opener_1']/opener_total)*100)}%"
    opener_2_perc = f"{round((ds2_field['opener_2']/opener_total)*100)}%"
    opener_3_perc = f"{round((ds2_field['opener_3']/opener_total)*100)}%"
    opener_4_perc = f"{round((ds2_field['opener_4']/opener_total)*100)}%"
    plot1_1_perc = f"{round((ds2_field['plot1_1']/plot1_total)*100)}%"
    plot1_2_perc = f"{round((ds2_field['plot1_2']/plot1_total)*100)}%"
    plot2_1_perc = f"{round((ds2_field['plot2_1']/plot2_total)*100)}%"
    plot2_2_perc = f"{round((ds2_field['plot2_2']/plot2_total)*100)}%"
    plot3_1_perc = f"{round((ds2_field['plot3_1']/plot3_total)*100)}%"
    plot3_2_perc = f"{round((ds2_field['plot3_2']/plot3_total)*100)}%"
    score_1_perc = f"{round((ds2_field['score_1']/score_total)*100)}%"
    score_2_perc = f"{round((ds2_field['score_2']/score_total)*100)}%"
    ff_1_perc = f"{round((ds2_field['ff_1']/favorite_food_total)*100)}%"
    ff_2_perc = f"{round((ds2_field['ff_2']/favorite_food_total)*100)}%"
    ff_3_perc = f"{round((ds2_field['ff_3']/favorite_food_total)*100)}%"
    ff_4_perc = f"{round((ds2_field['ff_4']/favorite_food_total)*100)}%"


#------------------------------------文字判斷主程式---------------------------------------#
    if(event.message.text=='可是沒有錢'):
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/0260da9db3d307b8d575033d26c954ba.png',
            preview_image_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/0260da9db3d307b8d575033d26c954ba.png'
            )
        )
    elif(event.message.text=='前有不得了的事物'):
        # 紀錄劇情1
        user_dict["image_plot"] = 1
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情1
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('回過神來\n已踏進藏壽司店裡\n選定位置坐下後\n有個鮮度君已在軌道上等著了'),
                TextSendMessage('當你疑惑著\n把手伸出想打開鮮度君時\n一道光芒宣洩而出！'),
                TextSendMessage('眼前景色一變\n人已置身於\n冰天雪地的山中小溪旁\n\n搞不清楚發生什麼事的你\n發現面前正有一隻碩大的巨熊緊盯著河面'),
                bt2_m,
            ]
        )
    elif(event.message.text=='Hey Bear!'):
        # 紀錄劇情1
        user_dict["image_plot"] = 1
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情1-1
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(
                    original_content_url='https://i.kym-cdn.com/entries/icons/original/000/029/198/Dark_Souls_You_Died_Screen_-_Completely_Black_Screen_0-2_screenshot.png',
                    preview_image_url='https://i.kym-cdn.com/entries/icons/original/000/029/198/Dark_Souls_You_Died_Screen_-_Completely_Black_Screen_0-2_screenshot.png'
                ),
            ]
        )
    elif(event.message.text=='(我躲)'):
        # 紀錄劇情1
        user_dict["image_plot"] = 1
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情1-2
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(
                    original_content_url='https://4.bp.blogspot.com/-wtVto1qA00w/WdyDHv4uhzI/AAAAAAABHZg/UE-oIxaLOM496PVTqClba515hnxQ0FD0ACLcBGAs/s800/animal_bear_kowai.png',
                    preview_image_url='https://4.bp.blogspot.com/-wtVto1qA00w/WdyDHv4uhzI/AAAAAAABHZg/UE-oIxaLOM496PVTqClba515hnxQ0FD0ACLcBGAs/s800/animal_bear_kowai.png'
                ),
                TextSendMessage('說此時那時快\n巨熊猛然起身！\n將手往溪中奮力一揮！\n\n一個黑色巨影從水中竄出！\n那是．．．！？'),
                bt3_m,                
            ]
        )
    elif(event.message.text=='喝啊～～～'):
        # 紀錄劇情2
        user_dict["image_plot"] = 2
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情2
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/yIR3rwG.jpg',
                    preview_image_url='https://i.imgur.com/yIR3rwG.jpg'
                ),
                TextSendMessage('在一番纏鬥之後\n魚影終於漸漸的接近船邊\n\n船長俐落的將牠綁在船邊\n開心地說到：\n賺大錢，是真的．．．\n那魚是．．．！？'),
                bt5_m,                
            ]
        )
    elif(event.message.text=='Ring-ding-ding-ding!'):
        # 紀錄劇情3
        user_dict["image_plot"] = 3
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情1-1
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(
                    original_content_url='https://i.kym-cdn.com/entries/icons/original/000/029/198/Dark_Souls_You_Died_Screen_-_Completely_Black_Screen_0-2_screenshot.png',
                    preview_image_url='https://i.kym-cdn.com/entries/icons/original/000/029/198/Dark_Souls_You_Died_Screen_-_Completely_Black_Screen_0-2_screenshot.png'
                ),
            ]
        )
    elif(event.message.text=='(這個香味是!)'):
        # 紀錄劇情3
        user_dict["image_plot"] = 3
        doc_ref.set(user_dict)

        # 停頓
        time.sleep(0.5)

        # 劇情3
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('：哦，你竟然知道咱最喜歡的食物，看來你早有準備'),
                TextSendMessage('鮮度君緩緩地掀起保鮮罩，裡面裝的是．．．？！'),
                bt7_m,            
            ]
        )
    elif(event.message.text=='@很有趣'):
        # 滿意度回應1
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('感謝您的支持！\n同時也感謝您耐心地玩到這裡！'),
                TextSendMessage('若想再重新遊玩\n可以將機器人封鎖後～\n再解除封鎖唷！'),
                TextSendMessage('其實製作這次的故事\n想要了解在進入壽司店時\n腦中閃過的第一個念頭\n究竟是想吃什麼呢？\n\n請幫我選出您的第一念頭\n待會可以一起來看看大家都選了什麼唷！'),
                fm2_m,            
            ]
        )
    elif(event.message.text=='@還好'):
        # 滿意度回應2
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('那我也沒辦法！\n時間實在不夠完整製作\n會不會改版就．．隨緣啦！\n阿哈哈．．．\n但還是感謝您耐心地玩到這裡！'),
                TextSendMessage('若想再重新遊玩\n可以將機器人封鎖後～\n再解除封鎖唷！'),
                TextSendMessage('其實製作這次的故事\n想要了解在進入壽司店時\n腦中閃過的第一個念頭\n究竟是想吃什麼呢？\n\n請幫我選出您的第一念頭\n待會可以一起來看看大家都選了什麼唷！'),
                fm2_m,            
            ]
        )
    elif(event.message.text in ff_list):
        line_bot_api.reply_message(
            event.reply_token, flex_out_fm3(ff_1_perc, ff_2_perc, ff_3_perc, ff_4_perc, favorite_food_total, total_people)
        )
    elif(event.message.text=='@我還要看更多！！'):
        # 全部統計表
        line_bot_api.reply_message(
            event.reply_token, Flex_out_fm_mix(total_people, opener_total, plot1_total, plot2_total, plot3_total, opener_1_perc, opener_2_perc, opener_3_perc, opener_4_perc, plot1_1_perc, plot1_2_perc, plot2_1_perc, plot2_2_perc, plot3_1_perc, plot3_2_perc)
        )
    elif(event.message.text=='@測試Flex'): 
        line_bot_api.reply_message(
            event.reply_token, [
                flex_out_fm3(ff_1_perc, ff_2_perc, ff_3_perc, ff_4_perc, favorite_food_total, total_people),
                Flex_out_fm_mix(total_people, opener_total, plot1_total, plot2_total, plot3_total, opener_1_perc, opener_2_perc, opener_3_perc, opener_4_perc, plot1_1_perc, plot1_2_perc, plot2_1_perc, plot2_2_perc, plot3_1_perc, plot3_2_perc),
            ]
        )
    elif(event.message.text=='@測試'):
        
        # line_bot_api.reply_message(event.reply_token, flex_message)
        # line_bot_api.reply_message(event.reply_token, fm1_m)

        # doc2_all_list = doc2_all.to_dict()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(str(doc2_all_list)))
        
        
    elif(event.message.text=='@參數'):
                # TextSendMessage('ds2_field: '+str(len(ds2_field))),
                # TextSendMessage('ds2_field_total: \n'+opener_1+'\n'+opener_2+'\n'+opener_3+'\n'+opener_4+'\n'+plot1_1+'\n'+plot1_2+'\n'+plot2_1+'\n'+plot2_2+'\n'+plot3_1+'\n'+plot3_2+'\n'+score_1+'\n'+score_2+'\n'+ff_1+'\n'+ff_2+'\n'+ff_3+'\n'+ff_4+'\n'),
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('user_dict:\n'+str(user_dict["image_plot"])+'\n'+str(user_dict["follow_total"])),
                TextSendMessage('user_event_dict:\n---opener---\n'+str(user_event_dict["opener_1"])+"\n"+str(user_event_dict["opener_2"])+"\n"+str(user_event_dict["opener_3"])+"\n"+str(user_event_dict["opener_4"])+"\n---plot1---\n"+str(user_event_dict["plot1_1"])+"\n"+str(user_event_dict["plot1_2"])+"\n---plot2---\n"+str(user_event_dict["plot2_1"])+"\n"+str(user_event_dict["plot2_2"])+"\n---plot3---\n"+str(user_event_dict["plot3_1"])+"\n"+str(user_event_dict["plot3_2"])+"\n---score---\n"+str(user_event_dict["score_1"])+"\n"+str(user_event_dict["score_2"])+"\n---favorite_food---\n"+str(user_event_dict["ff_1"])+"\n"+str(user_event_dict["ff_2"])+"\n"+str(user_event_dict["ff_3"])+"\n"+str(user_event_dict["ff_4"])),
                TextSendMessage(str(ds2_field)+'\n'),
                TextSendMessage(str(test1)+'\n'),
                TextSendMessage('percent: \n'+opener_1_perc+'\n'+opener_2_perc+'\n'+opener_3_perc+'\n'+opener_4_perc+'\n'+plot1_1_perc+'\n'+plot1_2_perc+'\n'+plot2_1_perc+'\n'+plot2_2_perc+'\n'+plot3_1_perc+'\n'+plot3_2_perc+'\n'+score_1_perc+'\n'+score_2_perc+'\n'+ff_1_perc+'\n'+ff_2_perc+'\n'+ff_3_perc+'\n'+ff_4_perc),
            ]
        )
    elif(event.message.text not in ret_dict_all):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage('若想再重新遊玩\n可以將機器人封鎖後～\n再解除封鎖唷！'),         
            ]
        )
    else:
        pass


# F03: 圖片辨識
from controllers.line_bot_controller import LineBotController
@handler.add(MessageEvent,ImageMessage)
def handle_line_image(event):
    # 劇情字典
    plot_dict = {
        1: '鮭魚all',
        2: '鮪魚all',
        3: '豆皮all',
    }
    # 辨識圖片
    ret = LineBotController.handle_image_message(event)

    # 取個資
    line_user_profile = line_bot_api.get_profile(event.source.user_id)
    bucket_name = "rabbitkm-0601-user-info"

    # 讀取firestore - 劇情資料
    db = firestore.Client()
    doc_ref = db.collection(u'rb-report-line-user').document(line_user_profile.user_id)
    doc = doc_ref.get()

    # 判斷資料是否存在
    # 存在: 開啟字典資料
    # 否則: 新增資料 (不排除資料庫被清空, 要重建資料.) + image_plot=0
    if doc.exists:
        user_dict = doc.to_dict()   
    else:
        user_dict = first_user_dict_save(line_user_profile, bucket_name, doc_ref)
    # 取image_plot

    # 判斷是否在劇情中
    if user_dict["image_plot"] in plot_dict:
        # 當prediction.max()<=0.6 (無法辨識AI模型)
        if ret == 'NOtOK':
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage('非常抱歉，機器人無法辨識這張圖片。'),  
                TextSendMessage('請換張圖片試試看！'), 
                ]
            )
        else:
            if ret == '鮭魚all' and user_dict["image_plot"] == 1:
                # 參數設為劇情2
                user_dict["image_plot"] = 2
                doc_ref.set(user_dict)

                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage('沒有錯～\n答案就是棕熊最愛的鮭魚\n濃厚的油脂感在嘴裡散開\n棕熊捕食的衝擊感仍在腦海中打轉\n.\n.\n.'),
                    TextSendMessage('雙手似乎迫不及待地\n再次伸向軌道上的鮮度君\n一道光芒宣洩而出！'),
                    TextSendMessage('眼前景色一變\n人已置身於乘風破浪的漁船上\n\n手裡不知為何握著釣竿\n身旁一位似乎船長的白鬍子老人正吆喝著你：'),
                    TextSendMessage('看清楚了，成敗之斯，在此一舉！\n今年的收入，就靠這把了！'),
                    bt4_m
                    ]
                )
            elif ret == '鮪魚all' and user_dict["image_plot"] == 2:
                # 參數設為劇情3
                user_dict["image_plot"] = 3
                doc_ref.set(user_dict)

                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage('沒有錯～\n那夢幻的(黑)鮪魚已含入口中\n無比的鮮味令人難以忘懷\n.\n.\n.'),
                    TextSendMessage('奇幻の冒險來到終章\n荷包君瘦了，肚子也撐了\n眼前的鮮度君散發出暗紅地光線'),
                    TextSendMessage('眼前景色一變\n人已置身於夜晚山中石徑上\n\n兩旁昏暗的石燈\n前方矗立著朱紅色的鳥居\n\n而鳥居後方不意外的有棟神社\n兩旁擺著狐狸石像。'),
                    TextSendMessage('此時從神社中傳出了女子的人聲：\n卑鄙的外鄉人啊！\n快速速離去，別怪咱不客氣。'),
                    bt6_m
                    ]
                )
            elif ret == '豆皮all' and user_dict["image_plot"] == 3:
                # 劇情結束
                user_dict["image_plot"] = 0
                doc_ref.set(user_dict)

                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage('沒錯～就是狐狸喜愛的豆皮\n難過地掉下兩行淚\n方才見過的女子已再也見不到\n眼前的視線逐漸模糊\n.\n.\n.'),
                    TextSendMessage('睜開雙眼\n猛然發現回到現實中\n\n原來\n我·還·在·加·班'),
                    fm1_m,
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage('這個似乎跟答案不一樣\n換張圖片試試吧'),
                    ]
                )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage('圖片辨識服務尚未啟用\n請嘗試觸發劇情\n感謝您的配合\n(ノ・ω・)ノヾ(・ω・ヾ)'),
            ]
        )

# run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))