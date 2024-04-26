import time
import requests

from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET


app = Flask(__name__)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证微信服务器
        token = '你的Token'
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        # 这里需要实现验证逻辑
        return echostr
    elif request.method == 'POST':
        # 处理微信消息
        msg = request.data
        # 解析XML消息
        root = ET.fromstring(msg)
        msg_type = root.find('MsgType').text
        from_user = root.find('FromUserName').text
        to_user = root.find('ToUserName').text

        if msg_type == 'text':
            content = root.find('Content').text
            # 这里可以根据消息内容进行处理，例如回复消息
            reply_content = '你发送的消息是：' + content
            reply_msg = f"""
            <xml>
            <ToUserName><![CDATA[{from_user}]]></ToUserName>
            <FromUserName><![CDATA[{to_user}]]></FromUserName>
            <CreateTime>{int(time.time())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{reply_content}]]></Content>
            </xml>
            """
            return reply_msg
        else:
            return 'success'

if __name__ == '__main__':
    app.run(debug=True)
