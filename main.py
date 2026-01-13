from flask import Flask, request, abort
import os
from dotenv import load_dotenv

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,

    # webhook event / message template
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselColumn,
    ImageCarouselTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
    DatetimePickerAction,

    # sending message
    PushMessageRequest,
    MulticastRequest,
    BroadcastRequest,

    # message type
    TextMessage,
    Emoji,
    VideoMessage,
    ImageMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    # FileMessage,

    # Imagemap
    ImagemapMessage,
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    MessageImagemapAction,
    URIImagemapAction,
    
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)

app = Flask(__name__)

load_dotenv()
configuration = Configuration(access_token=os.getenv('ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('WEBHOOK_HANDLER'))


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 加入好友
@handler.add(FollowEvent)
def handle_follow(event):
    print(f"Got {event.type} event!") # 32:55

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if event.message.text == 'postback':
            buttons_template = ButtonsTemplate(
                title='Postback Sample',
                text='Postback Action',
                actions=[
                    PostbackAction(label='Postback Action', text='Postback Action Button Clicked!', data='postback')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # line_bot_api = MessagingApi(api_client)
        # line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text=event.message.text)]
        #     )
        # )

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'postback':
        print('Postback event is triggered!')


# message event
@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # line_bot_api.reply_message(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text='reply message')] # 最多能有五則訊息
        #     )
        # )

        # result = line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text='reply message with http info')] # 最多能有五則訊息
        #     )
        # )

        # push message with http info
        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to=event.source.user_id, # reply token -> to; 可以是user_id也可以是group_id
        #         messages=[TextMessage(text='PUSH!')]
        #     )
        # )
    
        # broadcast message with http info
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='BROADCAST!')] # 不用指定傳給誰 -> 會傳給所有加入此官方帳號的user
        #     )
        # )

        # multicast message with http info
        line_bot_api.multicast_with_http_info(
            MulticastRequest(
                to=[event.source.user_id], # to 後面接一個陣列 -> 會傳給陣列中的所有user (不能包含group_id)
                # 從 terminal 的回傳訊息可以得知 user_id: Uc0f94a7b028bd926aee260740a0220e4 (Ex.)
                messages=[TextMessage(text='MULTICAST!')],
                notification_disabled=True # 靜音傳送 (關閉通知)
            )
        )

# message type
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text # 取得使用者輸入的訊息 不要耍白癡像我一樣忘記打這行
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == '文字':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='reply message')] # 最多能有五則訊息
                )
            )

        elif text == 'emoji':
            emojis = [
                Emoji(index=0, product_id='5ac2211e031a6752fb806d61', emoji_id='001'),
                Emoji(index=7, product_id='5ac2211e031a6752fb806d61', emoji_id='003')
                # 這裡的 index 要對應後面 ReplyMessageRequest 內 text 中 $ 的位置
            ]

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='$ 漢堡薯條 $', emojis=emojis)] # 要插入 emoji 的地方用 $ 號表示
                )
            )

        elif text == '貼圖':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(package_id='6362', sticker_id='11087922')]
                    # package_id 要和 sticker_id 一起使用
                )
            )

        elif text == '圖片':
            url = request.url_root + 'static/obama.png'
            url = url.replace('http://', 'https://') # line 不支援 http
            app.logger.info(url)

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [
                        ImageMessage(
                            original_content_url = 'https://upload.wikimedia.org/wikipedia/commons/0/08/Pencils_hb.jpg',
                            preview_image_url = 'https://upload.wikimedia.org/wikipedia/commons/0/08/Pencils_hb.jpg'
                            # original_content_url = url,
                            # preview_image_url = url
                        )
                        # 如果要傳送影片 -> 把 ImageMessage 改成 VideoMessage; 
                    ]
                )
            )

        # elif text == '影片':
        #     line_bot_api.reply_message(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages = [
        #                 VideoMessage(
        #                     original_content_url = 'https://example.com/video.mp4',
        #                     preview_image_url = 'https://example.com/video.jpg'
        #                 )
        #             ]
        #         )
        #     )

        elif text == '音訊':
            url = request.url_root + 'static/biubiubiu.m4a'
            url = url.replace('http://', 'https://') # line 不支援 http
            app.logger.info('url=' + url)

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [
                        AudioMessage(
                            original_content_url = url,
                            duration = 10000 # 音訊長度 (單位: 毫秒)
                        )
                    ]
                )
            )

        elif text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [
                        LocationMessage(
                            title = '位置',
                            address = '台北車站',
                            latitude = 25.0476667, # 緯度
                            longitude = 121.5165967 # 經度
                        )
                    ]
                )
            )
        
        elif text == 'confirm':
            confirm_template = ConfirmTemplate(
                text='文化幣用完了嗎？',
                actions=[
                    MessageAction(label='是', text='是！'),
                    MessageAction(label='否', text='否！')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm Sample',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        elif text == 'buttons':
            buttons_template = ButtonsTemplate(
                thumbnail_image_url='https://picx.zhimg.com/50/v2-10237b3d1106574cbd5187f73cf328e1_720w.gif?source=1def8aca',
                title='Demo',
                text='Description',
                actions=[
                    PostbackAction(label='回傳值', data='ping', display_text='傳了'),
                    MessageAction(label='傳「哈囉」', text='哈囉'),
                    URIAction(label='連結', uri='https://developers.line.biz/en/docs/messaging-api/message-types/#buttons-template'),
                    DatetimePickerAction(label='選擇時間', data='時間', display_text='done', mode='datetime')
                ]
            )
            template_message = TemplateMessage(
                alt_text='A button Template',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        elif text == 'carousel':
            carousel_template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://github.com/Dao1023/zhihu-emoji/blob/main/zhihu/emoji_13.png?raw=true',
                        title='Demo1',
                        text='Description1',
                        actions=[
                            URIAction(label='連結', uri='https://developers.line.biz/en/docs/messaging-api/message-types/#carousel-template')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic1.zhimg.com/50/v2-2e3a22fb33c8ceafdc3bc75ae0a240a3_720w.jpg?source=1def8aca',
                        title='Demo2',
                        text='Description2',
                        actions=[
                            URIAction(label='連結', uri='https://www.youtube.com/watch?v=Mw3cODdkaFM')
                        ]
                    )
                ]
            )
            template_message = TemplateMessage(
                alt_text='A carousel Template',
                template=carousel_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        elif text == 'image_carousel':
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://picx.zhimg.com/50/v2-f7de922bff135b8ebdd8cd9c7bc32c5d_720w.webp?source=1def8aca',
                        action=URIAction(
                            label='連結',
                            uri='https://developers.line.biz/en/docs/messaging-api/message-types/#image-carousel-template'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://pic1.zhimg.com/50/v2-2e3a22fb33c8ceafdc3bc75ae0a240a3_720w.jpg?source=1def8aca',
                        action=URIAction(
                            label='連結',
                            uri='https://www.youtube.com/watch?v=Mw3cODdkaFM'
                        )
                    )
                ]
            )
            template_message = TemplateMessage(
                alt_text='An image carousel Template',
                template=image_carousel_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        elif text == 'imagemap':
            url1 = request.url_root + 'static/imagemap'
            url1 = url1.replace('http://', 'https://')
            app.logger.info('url=' + url1)
            url2 = request.url_root + 'static/video.mp4'
            url2 = url2.replace('http://', 'https://')
            app.logger.info('url=' + url2)
            url3 = request.url_root + 'static/preview_image.png'
            url3 = url3.replace('http://', 'https://')
            app.logger.info('url=' + url3)

            imagemap_template = ImagemapMessage(
                base_url=url1,
                alt_text='An imagemap Template',
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=url2,
                    preview_image_url=url3,
                    area=ImagemapArea(x=0, y=0, width=1040, height=520),
                    external_link=ImagemapExternalLink(
                        link_uri='https://example.com',
                        label='點我看更多'
                    )
                ),
                actions=[
                    MessageImagemapAction(
                        area=ImagemapArea(x=0, y=0, width=1040, height=1040),
                        text='Hello'
                    ),
                    URIImagemapAction(
                        area=ImagemapArea(x=0, y=0, width=1040, height=1040),
                        uri='https://example.com'
                    )
                ]
            )
            template_message = TemplateMessage(
                alt_text='An imagemap Template',
                template=imagemap_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        
if __name__ == "__main__":
    app.run()