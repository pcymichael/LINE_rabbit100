from flask import Flask, request, abort
import requests, os
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)
from imgurpython import ImgurClient


app = Flask(__name__)

line_bot_api = LineBotApi('YOURKEY')
handler = WebhookHandler('YOURKEY')
client_id = 'YOURID'
client_secret = 'YOURKEY'
album_id = 'ALBUMID'
access_token = 'ACCESSTOKEN'
refresh_token = 'REFRESHTOKEN'

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
    app.logger.info("Request 身體: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))
    print("event.reply_token：", event.reply_token)
    print('event.message:', event.message)
    print('type(event.message):', type(event.message))
    
    if isinstance(event.message, TextMessage):
        print('event.message.type:', event.message.type)
        if event.message.text.lower()=='?' or event.message.text.lower()=='help':
            content = '目前可提供的功能有輸入)：\n(框框內的字可以更換)\n\n1. 油價\n2. 天氣查詢(ex: [高雄]天氣)\n3. 上傳圖片(直接丟圖片上來)\n4. 新番資訊(ex: [202007]新番)\n5. 股價查詢(ex: [2330]股價)'
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0

        if event.message.text.lower()=='油價':
            content = oil_price()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
        
        if event.message.text[-2:]=='天氣':
            content = get_weather(event.message.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    
        if event.message.text[-2:]=='新番':
            content = get_anime(event.message.text[:-2])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0

        if event.message.text[-2:]=='股價':
            print('event.message.text[-2:]:', event.message.text[-2:])
            print('event.message.text[:-2]:', event.message.text[:-2])
            content = get_stock(event.message.text[:-2])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0

    if isinstance(event.message, ImageMessage):
        print('event.message.type:', event.message.type)
        ''' get_message_content(message_id, timeout=None) -> Retrieve image, video, and audio data sent by users '''
        message_content = line_bot_api.get_message_content(event.message.id)    
        print('type(content):', type(message_content))
        ''' print('event.message.contentProvider:',event.message.contentProvider) 無contentProvider ''' 
        with open('./1.jpg', 'wb') as file:
            file.write(message_content.content)
            # print('message_content.content:', message_content.content)
        image_link = upload_image()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Successful\nImage URL：\n'+str(image_link)))
        return 0

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='命令錯誤\n請輸入 [?] 或 [help] ......'))

def oil_price():
    targe_url = 'https://gas.goodlife.tw/'
    response = requests.get(targe_url)
    response.encoding="utf8"
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.findAll('div', id="main")[0].text.replace('\n', '').split('(')[0]
    gas_price = soup.findAll("li", class_='main')[0].text.replace('\n\n', '').replace('\n', '').replace('＊','\n')
    items1 = soup.findAll('div', id='cpc')[0]
    cpc_price = items1.findAll('ul')[0].text.replace(' ', '').strip().replace('\n',' ')
    content1 = '{}\n{}\n{}'.format(title, gas_price, cpc_price)
    return content1

def get_weather(query_cont):
    try:
        targe_url = 'https://www.google.com.tw/search?q={query_cont}&oq={query_cont}&aqs=chrome.0.69i59.3551j0j7&sourceid=chrome&ie=UTF-8&hl=zh-TW'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        response = requests.get(targe_url.format(query_cont=query_cont), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        area, area_info = '', ''
        items1 = soup.findAll('span', {'role': 'heading'})[0]
        for i in items1:
            area += i.text+' '
        items2 = soup.find('div', class_='vk_gy vk_sh wob-dtl').findAll('div')[0:3]
        for i in items2:
            area_info += '\n'+i.text
        area_info = area_info.replace('\n', '', 1)
        content1 = '{}\n{}'.format(area, area_info)
    except Exception as e:
        print(e)
        content1 = '\n異常，請稍後在試......'
    return content1

def upload_image():
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album': album_id,
    }
    print("Uploading image... ")
    image=client.upload_from_path('./1.jpg', config=config, anon=False)
    os.remove('./1.jpg')
    print("Done\nThe image url is:", image['link'])
    return image['link']

def get_anime(query_cont):
    targe_url = 'https://acgsecrets.hk/bangumi/{query_cont}/'.format(query_cont=query_cont)
    print('URL:', targe_url)
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'cookie':'__cfduid=d6015f84b4cf9470aff325ea856dd0a531592115278'
    }
    response = requests.get(targe_url, headers=headers)
    response.encoding="utf8"
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('div', class_='anime_name')
    count=1
    content1 = '共 {} 筆資料：'   
    for i in items:
        content1+='\n'+str(count)+'. \t'+i.text
        count+=1
    return content1.format(count-1)

def get_stock(query_cont):
    targe_url = 'https://www.google.com/search?q=TPE+{query_cont}&oq=TPE+{query_cont}&aqs=chrome..69i57.9779j0j7&sourceid=chrome&ie=UTF-8&hl=zh-TW'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    print('targe_url.format(query_cont=query_cont:', targe_url.format(query_cont=query_cont))
    response = requests.get(targe_url.format(query_cont=query_cont), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    content1 = ''
    items = soup.findAll('g-card-section')
    content1+='\n'+items[1].div.text
    try:
        content1+='\n'+'成交價  '+items[1].span.text+'  '+items[1].find('span', class_='WlRRw IsqQVc fw-price-up').text   # 升值
    except:
        try:
            content1+='\n'+'成交價  '+items[1].span.text+'  '+items[1].find('span', class_='WlRRw IsqQVc fw-price-dn').text   # 貶值
        except:
            content1+='\n'+'成交價  '+items[1].span.text+'  '+items[1].find('span', class_='WlRRw IsqQVc fw-price-nc').text   # 無變化
    for i in items[3].findAll('tr'):    # 細項資料
        content1+='\n'+i.findAll('td')[0].text+'    '+i.findAll('td')[1].text
    return content1.replace('\n', '', 1)


if __name__ == "__main__":
    app.run()
    print('Runnung----------------------------------------------------')