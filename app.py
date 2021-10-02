# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

"""
"""
由kswdy借用樣板編輯，謝謝Ivan。
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import random

from linebot.models.responses import UserIds
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('QeDaDIs3LZJrWjeO/bCZHzHO1cnVjyWay1b37s0D72BhPkYv/2zxXWzvn1x7WhAfxadwnRQ4TLqqsGq2T+MDDO7FfYuEL73GlcYGno/+K2qRYJCuuTi+dQptQqsP2cXCHi07Z3zZNez1AHxnbQJ3UgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('a4bc5922cd9eefd8d623e8cf57b2d3bb')

line_bot_api.push_message('U28776fea18ea06ab1d83f9ca5a79c357', TextSendMessage(text='河河'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
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

#變數區
uservotes={}
yumeko=0, hatori=0, kemumaki=0, kidd=0

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    global hatori, yumeko, kemumaki,kidd
    msg = TextSendMessage(text=event.message.text)
    if re.match('河河',msg.text): #兩者類型要相同(msg是TextSendMessage類別，'河河'是字串)
        flex_message = TextSendMessage(text='蝦毀啦？',
            quick_reply=QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label="貼圖", text="給我個貼圖")),
                    QuickReplyButton(action=MessageAction(label="位置", text="給我個位置")),
                    QuickReplyButton(action=MessageAction(label="音訊", text="給我聲音")),
                    QuickReplyButton(action=MessageAction(label="圖片", text="我好愛你")),
                    QuickReplyButton(action=MessageAction(label="影片", text="GIJOE~~~")),
                    QuickReplyButton(action=MessageAction(label="秘密", text="告訴我秘密")),
                    QuickReplyButton(action=MessageAction(label="組圖訊息", text="給我大圖")),
                    QuickReplyButton(action=MessageAction(label="按鈕樣板", text="按鈕樣板")),
                    QuickReplyButton(action=MessageAction(label="多頁按鈕樣板", text="人氣投票")),
                    QuickReplyButton(action=MessageAction(label="確認樣板", text="確認樣板")),
                    QuickReplyButton(action=MessageAction(label="圖片選擇", text="圖片選擇")),
                    QuickReplyButton(action=MessageAction(label="自訂選單", text="自訂選單"))
                    ])) #至多13個
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('告訴我秘密',msg.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='秘密'))
    elif re.match('給我個貼圖', msg.text):
        # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        sticker = StickerSendMessage(package_id='1',sticker_id='1')
        line_bot_api.reply_message(event.reply_token, sticker)
    elif re.match('給我個位置', msg.text):
        line_bot_api.reply_message(event.reply_token, location_select(random.choice([0,1,2])))
    elif re.match('給我聲音', msg.text):
        audio_message = AudioSendMessage(
            original_content_url='https://www.dropbox.com/s/23ctbzfhqn4d5xs/G.I.JOE%20%E5%8F%B0%E7%81%A3%E8%8A%92%E6%9E%9C%20%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87%E5%AD%97%E5%B9%95%E7%89%88.mp3',
            duration=10000 #ms
        )
        line_bot_api.reply_message(event.reply_token, audio_message)
    elif re.match('GIJOE~~~',msg.text):
        line_bot_api.reply_message(event.reply_token, GIJOE(random.randrange(0,4)))
    elif re.match('我好愛你', msg.text):
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url='https://www.dropbox.com/s/de5d7pn3vbohgmz/Djgkb4D.jpg?dl=1',
            preview_image_url='https://www.dropbox.com/s/9sddkrdn84yd61v/dTf8Cao.jpeg?dl=1'
        ))
    elif re.match('人氣投票', msg.text):
        carousel_template_message = TemplateSendMessage(
            alt_text='人氣投票',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/2DCLYXG.jpg',
                        title='哈特利甘藏',
                        text='你逆\n目前'+str(hatori)+'票',
                        actions=[
                            URIAction(
                                label='角色介紹',
                                uri='https://zh.wikipedia.org/wiki/%E5%BF%8D%E8%80%85%E5%B0%8F%E9%9D%88%E7%B2%BE#%E5%93%88%E7%89%B9%E5%88%A9%E7%94%98%E8%97%8F%EF%BC%88-%7B%E6%9C%8D%E9%83%A8%E8%B2%AB%E8%94%B5%EF%BC%88%E3%83%8F%E3%83%83%E3%83%88%E3%83%AA%E3%82%AB%E3%83%B3%E3%82%BE%E3%82%A6%EF%BC%89%7D-%EF%BC%89'
                            ),
                            MessageAction(
                                label='投TA一票',
                                text='哈特利+1'
                            )]),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/tQTyhkc.jpg',
                        title='煙卷煙藏',
                        text='接招吧，哈特利！\n目前'+str(kemumaki)+'票',
                        actions=[
                            URIAction(
                                label='角色介紹',
                                uri='https://zh.wikipedia.org/wiki/%E5%BF%8D%E8%80%85%E5%B0%8F%E9%9D%88%E7%B2%BE#%E7%85%99%E5%8D%B7%E7%85%99%E8%97%8F%EF%BC%88-%7B%E3%82%B1%E3%83%A0%E3%83%9E%E3%82%AD%E3%83%BB%E3%82%B1%E3%83%A0%E3%82%BE%E3%82%A6%7D-%EF%BC%89'
                            ),
                            MessageAction(
                                label='投TA一票',
                                text='煙卷+1'
                            )]),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/SzCZbbT.jpg',
                        title='河合夢子',
                        text='辣個和我很像的女人\n目前'+str(yumeko)+'票',
                        actions=[
                            URIAction(
                                label='角色介紹',
                                uri='https://zh.wikipedia.org/wiki/%E5%BF%8D%E8%80%85%E5%B0%8F%E9%9D%88%E7%B2%BE#%E6%B2%B3%E5%90%88%E5%A4%A2%E5%AD%90%EF%BC%88-%7B%E6%B2%B3%E5%90%88%E5%A4%A2%E5%AD%90%EF%BC%88%E3%81%8B%E3%82%8F%E3%81%84_%E3%82%86%E3%82%81%E3%81%93%EF%BC%89%7D-%EF%BC%89'
                            ),
                            MessageAction(
                                label='投TA一票',
                                text='夢子+1'
                            )]),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/TIoZA0P.jpg',
                        title='布萊德·基德',
                        text='我叫基德是個忍者\n目前'+str(kidd)+'票',
                        actions=[
                            URIAction(
                                label='角色介紹',
                                uri='https://zh.moegirl.org.cn/index.php?title=%E4%B8%8D%E8%A6%81%E7%9E%8E%E6%8E%B0%E5%A5%BD%E5%90%97&variant=zh-tw'
                            ),
                            MessageAction(
                                label='投TA一票',
                                text='基德+1'
                            )]),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif re.match('哈特利+1',msg.text):
        if event.source.userID not in uservotes:
            uservotes[event.source.userID]=1
            hatori+=1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='哈特利目前有'+str(hatori)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        elif uservotes[event.source.userID]<=2:
            hatori+=1
            uservotes[event.source.userID]=uservotes[event.source.userID]+1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='哈特利目前有'+str(hatori)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你已經沒票了，窮鬼'))
    elif re.match('煙卷+1',msg.text):
        if event.source.userID not in uservotes:
            uservotes[event.source.userID]=1
            kemumaki+=1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='煙卷目前有'+str(hatori)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        elif uservotes[event.source.userID]<=2:
            kemumaki+=1
            uservotes[event.source.userID]=uservotes[event.source.userID]+1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='煙卷目前有'+str(kemumaki)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你已經沒票了，窮鬼'))
    elif re.match('夢子+1',msg.text):
        if event.source.userID not in uservotes:
            uservotes[event.source.userID]=1
            yumeko+=1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='夢子目前有'+str(yumeko)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        elif uservotes[event.source.userID]<=2:
            yumeko+=1
            uservotes[event.source.userID]=uservotes[event.source.userID]+1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='夢子目前有'+str(yumeko)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你已經沒票了，窮鬼'))
    elif re.match('基德+1',msg.text):
        if event.source.userID not in uservotes:
            uservotes[event.source.userID]=1
            kidd+=1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='基德目前有'+str(kidd)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        elif uservotes[event.source.userID]<=2:
            kidd+=1
            uservotes[event.source.userID]=uservotes[event.source.userID]+1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='基德目前有'+str(kidd)+'票，你已投'+str(uservotes[event.source.userID])+'票'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你已經沒票了，窮鬼'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='？？？'))

def location_select(n=0):
    if n==1:
        t='坑錢學店'
        a='天主教輔仁大學'
        lat=25.037191131186056
        lon=121.4323050978726
    elif n==2:
        t='愛與希望'
        a='幸福，就是這麼簡單'
        lat=35.363401824199606
        lon=138.73106168223435
    else:
        t='日治時期的古蹟'
        a='總統府'
        lat=25.040213810016002
        lon=121.51238385108306
    return LocationSendMessage(title=t,address=a,latitude=lat ,longitude=lon)

def GIJOE(n=0):            
    if n==1:
        return VideoSendMessage( #無法直接從gd擷取，imgur網址尾+格式
            original_content_url='https://i.imgur.com/BUMXREp.mp4',
            preview_image_url='https://imgur.com/qDlvKo0.png'
        )
    elif n==2:
         return VideoSendMessage( #網址尾?dl=1 直接下載的意思
            original_content_url='https://www.dropbox.com/s/3fyy1gziw1rkvf6/%E5%81%A5%E5%BA%B7%E6%8D%90.mp4?dl=1',
            preview_image_url='https://www.dropbox.com/s/59o2vfg6kqek1sp/162306842871675_P8231924.png?dl=1'
        )
    elif n==3:
        return TextSendMessage(text='https://youtu.be/jMkWfMt1j08') #丟連結也會產生預覽
    else:
        return TextSendMessage(text='GIJOE~~~~!')

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
