from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from DcardHot import Hot

app = Flask(__name__)

#填入Channel access token
line_bot_api = LineBotApi('2Gfz3rpTSv+MWV3u+6OZHTvYZgpp8mGiiJyfeZMkZ5Stx4nWK5uM09vZtTJSfL4xaCqn4TPvk+dOBjqHYnfUQ5uYb0xUM08IBxMCi34YtdeFasz4Yl/aaNkHmJkfYJVsvqDGIqhMxhDHfvjbvG6CDgdB04t89/1O/w1cDnyilFU=')
#填入Channel secret
handler = WebhookHandler('83e37681ed8d663191d7c679e323de3f')


@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    li_Dcard=Hot()
    # str_Dcard=""
    # str_Dcard="\n".join(li_Dcard)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=li_Dcard[0]))

if __name__ == "__main__":
    app.run()
    