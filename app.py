from os import getenv
from flask import Flask, json, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TemplateMessage, ButtonsTemplate, PostbackAction, ConfirmTemplate,
    CarouselColumn, ImageCarouselColumn, MessageAction, URIAction,
    DatetimePickerAction, CarouselTemplate, ImageCarouselTemplate,
    FlexMessage, FlexContainer, MessageImagemapAction, URIImagemapAction,
    ImagemapArea, ImagemapBaseSize, ImagemapExternalLink,
    ImagemapVideo, ImagemapMessage
)
from linebot.v3.webhooks import MessageEvent, FollowEvent, PostbackEvent, TextMessageContent
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
getenv('.env')
configuration = Configuration(
    access_token=getenv('ACCESS_TOKEN'),
)
handler = WebhookHandler(getenv('WWEBHOOK_HEANDER'))


def send_reply_message(api_client, reply_token, template_message):
    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[template_message]
        )
    )
    
    
def get_flex_message():
    line_flex_json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://i.pinimg.com/736x/89/df/1c/89df1cac060af5f229ca7b2dc6b73dae.jpg",
            "size": "full",
            "aspectRatio": "4:4",
            "aspectMode": "cover",
            "action": {"type": "uri", "uri": "https://line.me/"}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl",
                    "contents": [
                        {"type": "span", "text": "哈哈哈"},
                        {"type": "span", "text": "讚喔", "size": "sm"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {"type": "icon", "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"},
                        {"type": "icon", "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"},
                        {"type": "icon", "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"},
                        {"type": "icon", "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"},
                        {"type": "icon", "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"},
                        {"type": "text", "text": "4.0", "size": "sm",
                            "color": "#999999", "margin": "md", "flex": 0}
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": "這是啥",
                                    "color": "#aaaaaa", "size": "sm", "flex": 2},
                                {"type": "text", "text": "哇哇哇原來在這裡", "wrap": True,
                                    "color": "#666666", "size": "sm", "flex": 5}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": "取啥名字",
                                    "color": "#aaaaaa", "size": "sm", "flex": 3},
                                {"type": "text", "text": "啊哈哈哈啊哈", "wrap": True,
                                    "color": "#666666", "size": "sm", "flex": 5}
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {"type": "button", "style": "link", "height": "sm", "action": {
                    "type": "uri", "label": "IG", "uri": "https://www.instagram.com/guobei_zih_yan/"}},
                {"type": "button", "style": "link", "height": "sm", "action": {
                    "type": "uri", "label": "YT", "uri": "https://www.youtube.com/@NTUEIRC"}}
            ],
            "flex": 0
        }
    }
    return FlexMessage(
        alt_text='詳細說明',
        contents=FlexContainer.from_json(json.dumps(line_flex_json))
    )


MESSAGE_HANDLERS = {
    'ask me': lambda: TemplateMessage(
        alt_text='Confirm Sample',
        template=ConfirmTemplate(
            text='are u gay?',
            actions=[
                MessageAction(label='Yes', text='Yes!'),
                MessageAction(label='No', text='No!'),
            ]
        )
    ),
    'choose vocation': lambda: TemplateMessage(
        alt_text='Carousel Sample',
        template=ButtonsTemplate(
            thumbnailImageUrl='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoEywooNqlCh2h3ukw8RMfV2QLk-L88-dac2V4fszxeixGlXCDdbws96ciWXJfJ-FpcKc&usqp=CAU',
            title='Regular Show',
            text='What do you want to do in your vocation?',
            actions=[
                MessageAction(label='Go Hiking', text='Go Hiking'),
                URIAction(
                    label='View Detail', uri='https://zh.wikipedia.org/wiki/%E6%AD%A3%E8%A6%8F%E7%9A%84%E6%88%8F%E8%BF%B9'),
                DatetimePickerAction(label='Select Date', data='action=selct_date',
                                     mode='date', initial='2024-06-01', max='2024-12-31', min='2024-01-01')
            ]
        )
    ),
    'choose animate': lambda: TemplateMessage(
        altText="Carousel Sample",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnailImageUrl='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRihvEEbUzftwQlEWbBdYyT5nVpO5XiXlHoCw&s',
                    title='Regular Show',
                    text='Choose your character',
                    actions=[
                        MessageAction(label='Mordecai', text='Mordecai'),
                        MessageAction(label='Rigby', text='Rigby'),
                        MessageAction(label='Benson', text='Benson'),
                    ]
                ),
                CarouselColumn(
                    thumbnailImageUrl='https://static0.cbrimages.com/wordpress/wp-content/uploads/2020/10/princess-bubblegum.jpg?q=50&fit=crop&w=825&dpr=1.5',
                    title='Adventure Time',
                    text='Choose your character',
                    actions=[
                        MessageAction(label='Finn', text='Finn'),
                        MessageAction(label='Jake', text='Jake'),
                        MessageAction(label='Princess Bubblegum',
                                      text='Princess Bubblegum'),
                    ]
                )
            ]
        )
    ),
    'choose image': lambda: TemplateMessage(
        alt_text='Image Carousel Sample',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    imageUrl='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRihvEEbUzftwQlEWbBdYyT5nVpO5XiXlHoCw&s',
                    action=MessageAction(label='Mordecai', text='Mordecai')
                ),
                ImageCarouselColumn(
                    imageUrl='https://static0.cbrimages.com/wordpress/wp-content/uploads/2020/10/princess-bubblegum.jpg?q=50&fit=crop&w=825&dpr=1.5',
                    action=MessageAction(label='Princess B', text='Princess B')
                )
            ]
        )
    ),
    'postback': lambda: TemplateMessage(
        alt_text='Postback Sample',
        template=ButtonsTemplate(
            title='Postback Sample',
            text='Postback Action',
            actions=[PostbackAction(
                label='Postback Action', text='Postback Action Button Clicked!', data='postback')]
        )
    ),
    'flex': get_flex_message,
}


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        text = event.message.text

        if text in MESSAGE_HANDLERS:
            handler_func = MESSAGE_HANDLERS[text]
            template_message = handler_func() if callable(handler_func) else handler_func
            send_reply_message(api_client, event.reply_token, template_message)

        elif text == 'imagemap':
            url1 = request.url_root + 'static/imagemap'
            url1 = url1.replace("http", "https")
            url2 = request.url_root + 'static/video.mp4'
            url2 = url2.replace("http", "https")
            url3 = request.url_root + 'static/preview_image.png'
            url3 = url3.replace("http", "https")

            app.logger.info(f"urls: {url1}, {url2}, {url3}")

            imagemap_message = ImagemapMessage(
                base_url=url1,
                alt_text='this is an imagemap',
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=url2,
                    preview_image_url=url3,
                    area=ImagemapArea(x=0, y=0, width=1040, height=520),
                    external_link=ImagemapExternalLink(
                        link_uri='https://www.youtube.com/@bigdatantue',
                        label='點我看更多',
                    ),
                ),
                actions=[
                    URIImagemapAction(
                        type="uri",
                        linkUri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=',
                        area=ImagemapArea(x=0, y=520, width=520, height=520)
                    ),
                    MessageImagemapAction(
                        type="message",
                        text='這是fb網頁https://www.facebook.com/NTUEBIGDATAEDU',
                        area=ImagemapArea(x=520, y=520, width=520, height=520)
                    )
                ]
            )
            send_reply_message(api_client, event.reply_token, imagemap_message)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'postback':
        print('Postback event is triggered')


if __name__ == "__main__":
    app.run()
