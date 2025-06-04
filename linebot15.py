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
        sendPizza(event)
    elif msg == '@yes':
        sendYes(event)
    elif msg == '@轉盤':
        sendCarousel(event)
    elif msg == '@確認':
        sendConfirm(event)
    elif msg == '@圖片轉盤':
        sendImgCarousel(event)
    elif msg == '@按鈕':
        sendButton(event)
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
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://ibb.co/Rp8spdjz',
                title='按鈕樣板示範',
                text='請選擇：',
                actions=[
                    MessageTemplateAction(
                        label='文字訊息!',
                        text='@fwee'
                    ),
                    URITemplateAction(
                        label='連結網頁',
                        uri='http://www.e-happy.com.tw'
                    ),
                    PostbackTemplateAction(
                        label='回傳訊息',
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
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://ibb.co/0RPKY2Hp',
                        title='唇彩',
                        text='讓fwee更貼近你的心情',
                        actions=[
                            MessageTemplateAction(
                                label='點這裡',
                                text='fwee熱賣系列唇彩'
                            ),
                            URITemplateAction(
                                label='連結進入fwee的世界',
                                uri='https://fwee.kr/product/list.html?cate_no=30'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item=唇彩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
                        title='底妝',
                        text='讓fwee成為你的無所畏懼',
                        actions=[
                            MessageTemplateAction(
                                label='點這裡',
                                text='fwee輕薄透亮底妝'
                            ),
                            URITemplateAction(
                                label='連結進入fwee的世界',
                                uri='https://fwee.kr/product/list.html?cate_no=53'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
                                data='action=sell&item=底妝'
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
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4QfKuz1.png',
                        action=MessageTemplateAction(
                            label='唇彩',
                            text='為您推薦熱門唇彩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/qaAdBkR.png',
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

def sendPizza(event):
    try:
        message = TextSendMessage(
            text='I am fwee Feel Your Moment, fwee'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝您的購買，\n我們將盡快寄出商品。'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata):
    try:
        text1 = '感謝您選擇fwee，我們將盡快為您寄出。' 
        message = TextSendMessage(text=text1)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendBack_sell(event, backdata):
    try:
        message = TextSendMessage(text='點選的是賣 ' + backdata.get('item'))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()

