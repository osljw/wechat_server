import time
import requests
import hashlib

from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET


app = Flask(__name__)


def check_signature(token, signature, timestamp, nonce):
    # 将token、timestamp、nonce三个参数进行字典序排序
    params = sorted([token, timestamp, nonce])
    # 将排序后的参数拼接成一个字符串
    params_str = ''.join(params)
    # 使用sha1算法对字符串进行哈希
    hash_code = hashlib.sha1(params_str.encode('utf-8')).hexdigest()
    # 将计算出的哈希值与signature进行比较，如果相同则验证通过
    return hash_code == signature

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证微信服务器
        token = '你的Token' # 设置与开发 -> 基本配置 -> 服务器配置 -> 令牌(Token)
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        if check_signature(token, signature, timestamp, nonce):
            return echostr
        else:
            return '验证失败'
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
