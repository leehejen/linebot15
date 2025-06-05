from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent, TextSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, PostbackTemplateAction, URITemplateAction,
    CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
)
from urllib.parse import parse_qsl

import os

app = Flask(__name__)


line_bot_api = LineBotApi(os.getenv('Channel_Access_Token'))
handler = WebhookHandler(os.getenv('Channel_Secret'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '@fwee':
        sendFweeRecommend(event)
    elif msg == '@進度查詢':
        sendBack_buy(event)
    elif msg == '@商品推薦':
        sendCarousel(event)
    elif msg == '@訂單確認':
        sendConfirm(event)
    elif msg == '@更多商品':
        sendImgCarousel(event)
    elif msg == '@最新資訊':
        sendButton(event)
    elif msg == '@yes':
        sendYes(event)
    elif msg == 'fwee熱賣系列唇彩':
        sendrecommand1(event)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入指定指令。'))

@handler.add(PostbackEvent)
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))
    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)

def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='最新資訊',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.postimg.cc/C1gtjWbL/temp-Image-Fw8-QF5.avif',
                title='最新資訊',
                text='請選擇：',
                actions=[
                     URITemplateAction(
                        label='賣場連結',
                        uri='https://shopee.tw/fwee.official.tw'
                    ),
                    URITemplateAction(
                        label='官網連結',
                        uri='https://fwee.kr/?srsltid=AfmBOopZBEPJgaN6z6IzixXSj3S1prqa9jSieOBI07Kp_OccCmXmJHiN'
                    ),
                    PostbackTemplateAction(
                        label='訂單確認',
                        data='action=buy'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendConfirm(event):
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎？',
                actions=[
                    MessageTemplateAction(
                        label='是',
                        text='@yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='商品推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.postimg.cc/sDRXt9tZ/temp-Imageg1m-UZf.avif',
                        title='唇彩',
                        text='讓fwee更貼近你的心情',
                        actions=[
                            MessageTemplateAction(
                                label='點這裡',
                                text='fwee熱賣系列唇彩'
                            ),
                            URITemplateAction(
                                label='連結進入fwee的世界',
                                uri='https://shopee.tw/fwee.official.tw?shopCollection=251062841#product_list'
                            ),
                           
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.postimg.cc/fbpdpN8D/temp-Imageng-Pf9f.avif',
                        title='底妝',
                        text='讓fwee成為你的無所畏懼',
                        actions=[
                            MessageTemplateAction(
                                label='點這裡',
                                text='fwee輕薄透亮底妝'
                            ),
                            URITemplateAction(
                                label='連結進入fwee的世界',
                                uri='https://shopee.tw/fwee.official.tw?shopCollection=251023033#product_list'
                            ),
            
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendImgCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='商品推薦',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.postimg.cc/9fh5pRhh/temp-Imageep-LB9a.avif',
                        action=MessageTemplateAction(
                            label='唇彩',
                            text='fwee熱賣系列唇彩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.postimg.cc/vmFMN25C/temp-Imagew73-HEl.avif',
                        action=PostbackTemplateAction(
                            label='底妝',
                            data='action=sell&item=為您推薦熱門底妝'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

from linebot.models import FlexSendMessage

def sendFweeRecommend(event):
    try:
        message = FlexSendMessage(
            alt_text='@fwee',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Feel Your Moment, fwee",
                            "weight": "bold",
                            "size": "lg",
                            "wrap": True
                        },
                        {
                            "type": "image",
                            "url": "https://i.postimg.cc/WzybsBHP/temp-Image-A3-Aw-Ir.avif",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "uri": "https://fwee.kr/?srsltid=AfmBOoqyH6sukQDBVX4PIqzbPGbE-3N5lqu-3t9JKbNtqaMR_m_00x_d"
                            },
                            "margin": "md"
                        }
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝您的購買，\n我們將盡快寄出商品。'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata=None):
    try:
        message = TextSendMessage(
            text='感謝您的購買，商品將盡快寄出\n'
                 '🧾 訂單查詢結果如下：\n\n'
                 '📦 訂單編號：#FWEE20250603\n'
                 '💄 購買產品：fwee 熱賣系列唇彩 - 柔霧玫瑰\n'
                 '🚚 出貨狀態：已出貨（黑貓宅急便）\n'
                 '📅 出貨日期：2025/06/03\n'
                 '🔍 查詢連結：\nhttps://shopee.tw/user/purchase/list'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_sell(event, backdata):
    try:
        message = TextSendMessage(text='點選的是 ' + backdata.get('item'))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendrecommand1(event):
    try:
        message = FlexSendMessage(
            alt_text='fwee 熱賣色號推薦',
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.postimg.cc/k4WTJnmt/temp-Imagenx2-Yu-S.avif",
                            "size": "full",
                            "aspectRatio": "1.51:1",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "uri": "https://shopee.tw/fwee-唇頰兩用布丁膏-—-30色-5g-i.1152063847.24473108309?sp_atk=1e5c9706-7a96-48d0-bfcf-74e528f17846&xptdk=1e5c9706-7a96-48d0-bfcf-74e528f17846"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ND03 Without",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "立即購買",
                                        "uri": "https://shopee.tw/fwee-唇頰兩用布丁膏-—-30色-5g-i.1152063847.24473108309?sp_atk=1e5c9706-7a96-48d0-bfcf-74e528f17846&xptdk=1e5c9706-7a96-48d0-bfcf-74e528f17846"
                                    },
                                    "style": "primary"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.postimg.cc/bJnBZxQr/temp-Image-Lb357-Z.avif",
                            "size": "full",
                            "aspectRatio": "1.51:1",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "uri": "https://shopee.tw/fwee-唇頰兩用布丁膏-—-30色-5g-i.1152063847.24473108309?sp_atk=1e5c9706-7a96-48d0-bfcf-74e528f17846&xptdk=1e5c9706-7a96-48d0-bfcf-74e528f17846"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "PK01 Baby",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "立即購買",
                                        "uri": "https://shopee.tw/fwee-唇頰兩用布丁膏-—-30色-5g-i.1152063847.24473108309?sp_atk=1e5c9706-7a96-48d0-bfcf-74e528f17846&xptdk=1e5c9706-7a96-48d0-bfcf-74e528f17846"
                                    },
                                    "style": "primary"
                                }
                            ]
                        }
                    },
        
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.postimg.cc/rwBhvh0m/temp-Image-Ly-Yua-P.avif",
                            "size": "full",
                            "aspectRatio": "1.51:1",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "探索更多色號",
                                    "weight": "bold",
                                    "size": "xl",
                                    "align": "center"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "前往完整賣場",
                                        "uri": "https://shopee.tw/fwee.official.tw"
                                    },
                                    "style": "primary"
                                }
                            ]
                        }
                    }
                ]
            }
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

if __name__ == '__main__':
    app.run()

