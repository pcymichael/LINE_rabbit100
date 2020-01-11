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
    str_Dcard="\n".join(li_Dcard)
    st="https://www.dcard.tw/f/entertainer/p/232862065-當李秀滿在聊天群向RedVelvet詢問對服裝的看法時！\nhttps://www.dcard.tw/f/trending/p/232859612-我知道已經很多篇了-但我還是要說麻煩大家1／11回家投票��"
    st1="https://www.dcard.tw/f/relationship/p/232861828-男生很少會主動提分手"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=st+st1))
    

if __name__ == "__main__":
    app.run()
    