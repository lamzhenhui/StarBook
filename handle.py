import hashlib
import web
import time
import requests
class Handle(object):
    def GET(self):
        try:
            data = web.input()
            web
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            # print(signature, 'wxgzh2025')
            token = "wxgzh2025" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode("utf-8"))
            sha1.update(list[1].encode("utf-8"))
            sha1.update(list[2].encode("utf-8"))
            hashcode = sha1.hexdigest() #获取加密串
            if hashcode == signature:
                return echostr
            else:
                print('??')
                return ""
        except Exception as Argument:
            print(Argument)
            return Argument
    def POST(self):
        try:
            data = web.input()
            print(data, 'data print')
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce

            # echostr = data.echostr
            # print()
            # print(signature, 'wxgzh2025')
            token = "wxgzh2025" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode("utf-8"))
            sha1.update(list[1].encode("utf-8"))
            sha1.update(list[2].encode("utf-8"))
            hashcode = sha1.hexdigest() #获取加密串
            print(signature,hashcode )
            if hashcode == signature:
                # import hashlib
                # return echostr
                print(web.data())
                handle_message(web.data())
                print("消息处理完毕")
            else:
                print('??')
                return ""
        except Exception as Argument:
            print(Argument, '异常信息')
            return Argument
# from flask import Flask, request

# app = Flask(__name__)
# TOKEN = "your_token"

# @app.route('/wechat', methods=['GET', 'POST'])
# def wechat():
#     if request.method == 'GET':
#         signature = request.args.get('signature')
#         timestamp = request.args.get('timestamp')
#         nonce = request.args.get('nonce')
#         echostr = request.args.get('echostr')

#         # 校验逻辑
#         s = ''.join(sorted([TOKEN, timestamp, nonce]))
#         if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
#             return echostr  # 返回验证成功的 echostr
#         return "Unauthorized"

#     elif request.method == 'POST':
#         # 处理用户消息
#         return handle_message(request.data)

def handle_message(xml_data):
    # 解析 XML 数据，处理用户发送的文本消息
    # 例如，用户发送的文本消息格式如下：
    # <xml>
    #   <ToUserName><![CDATA[to_user]]></ToUserName>
    #   <FromUserName><![CDATA[from_user]]></FromUserName>
    #   <CreateTime>123456789</CreateTime>
    #   <MsgType><![CDATA[text]]></MsgType>
    #   <Content><![CDATA[hello]]></Content>
    #   <MsgId>1234567890123456</MsgId>
    # </xml>

    # 示例解析逻辑
    print("开始处理消息")
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)
    msg_type = root.find('MsgType').text
    if msg_type == 'text':
        content = root.find('Content').text
        print(content, '用户发送的消息')
        from_user = root.find('FromUserName').text
        to_user = root.find('ToUserName').text

        # 构造回复消息
        content = '你好, 有什么可以帮到您?'
        reply = f"""
        <xml>
          <ToUserName><![CDATA[{from_user}]]></ToUserName>
          <FromUserName><![CDATA[{to_user}]]></FromUserName>
          <CreateTime>{int(time.time())}</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[您发送的消息是：{content}]]></Content>
        </xml>
        """
        print(reply)
        return reply
    return "success"  # 无需回复消息时，返回 success

