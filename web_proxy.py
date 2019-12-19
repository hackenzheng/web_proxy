#coding:utf-8
from socket import *

# 创建socket，绑定到端口，开始监听
tcpSerPort = 8899
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# 测试地址
# http://www.hitsz.edu.cn/UserFiles/banner/orig/1574407474192.jpg
# https://2.python-requests.org//zh_CN/latest/user/quickstart.html

# Prepare a server socket
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)

import requests

while True:
    # 开始从客户端接收请求
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(4096).decode()

    try:
        # 在代理服务器上创建一个tcp socket
        msg_list = message.split()
        if not msg_list:
            continue
        filename = msg_list[1].strip('/')
        print('Creating socket on proxyserver')
        if not filename.startswith('http'):
            filename = 'http://' + filename

        ret = requests.get(filename)

        h = "HTTP/1.1 200 OK\r\n"
        for k, v in ret.headers.items():
            # t_h += '{k}: {v}\r\n'.format(k=k, v=v)
            if k in ['Content-Type', 'Content-Length', 'Cache-Control', 'Content-Language', 'X-Content-Type-Options'
                     'Transfer-Encoding', 'Connection', 'Date', 'X-Frame-Options', 'Server', 'Set-Cookie']:
                h += '{k}: {v}\r\n'.format(k=k,v=v)
        h += '\r\n'
        h += ret.content

        tcpCliSock.sendall(h)
    except Exception as e:
        print(e)

    tcpCliSock.close()
tcpSerSock.close()



# import  socket
# se = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host=" /jobrecord/login/index.do"
# se.connect(("192.168.1.41",91))
# try:
#          se.send("GET /jobrecord/login/index.do HTTP/1.1\r\n")
#          se.send("Host: 192.168.1.41:91\r\n")
#          se.send("Connection: keep-alive\r\n")
#          se.send("Cache-Control: max-age=0\r\n")
#          se.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n")
#          se.send("Upgrade-Insecure-Requests: 1\r\n")
#          se.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n")
#          se.send("Accept-Encoding: gzip, deflate, sdch\r\n")
#          se.send("Accept-Language: zh-CN,zh;q=0.8\r\n")
#          se.send("Cookie: JSESSIONID=8E827CDF1932CAC60C4D4AA4DD39C171; sid=a1m649tme0i2bu00b03rbnc806\r\n\r\n")
# except socket.error ,e:
#           print "Error sending data:%s" % e
# buffer = []
# while True:
#           d = se.recv(1024)
#           if d:
#                     buffer.append(d)
#           else:
#                     break
# data = ''.join(buffer)
# se.close()
# header,html = data.split('\r\n\r\n',1)
# print header
# with open('D:\\sina.html','wb') as f:
#        f.write(html)
