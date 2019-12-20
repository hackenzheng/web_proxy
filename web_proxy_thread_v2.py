#coding:utf-8
from socket import *
import threading
import time
import logging

# 创建socket，绑定到端口，开始监听
tcpSerPort = 8899
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# 测试地址
# http://www.hitsz.edu.cn/UserFiles/banner/orig/1574407474192.jpg
# https://2.python-requests.org//zh_CN/latest/user/quickstart.html


cache_map = {}

import requests

def workers(tcpSerSock):
    tcpCliSock, addr = tcpSerSock.accept()
    print('thread name is %s ......' % (threading.current_thread().name))
    message = tcpCliSock.recv(4096).decode()
    try:
        # 在代理服务器上创建一个tcp socket
        msg_list = message.split()
        if not msg_list:
            return
        filename = msg_list[1].strip('/')
        if not filename.startswith('http'):
            filename = 'http://' + filename

        ret = ''
        if filename in cache_map:
            print("hit cache========")
            ret = cache_map[filename]
        else:
            r_get = requests.get(filename)

            ret = "HTTP/1.1 200 OK\r\n"
            for k, v in r_get.headers.items():
                if k in ['Content-Type', 'Content-Length', 'Cache-Control', 'Content-Language', 'X-Content-Type-Options'
                         'Transfer-Encoding', 'Connection', 'Date', 'X-Frame-Options', 'Server', 'Set-Cookie']:
                    ret += '{k}: {v}\r\n'.format(k=k,v=v)
            ret += '\r\n'
            ret += r_get.content
            cache_map[filename] = ret

        print('start send data\n')
        logging.info('start send data\n')
        tcpCliSock.sendall(ret)
        tcpCliSock.close()
        print('finish send, sleep 10s')
        time.sleep(10)
    except Exception as e:
        print('exception:')
        print(e)
        tcpCliSock.close()

if __name__ == '__main__':
    # Prepare a server socket
    tcpSerSock.bind(('', tcpSerPort))
    tcpSerSock.listen(5)

    # 多个线程同时监听,而不是主线程负责监听
    try:

        # 开始从客户端接收请求
        print('waiting for client connect...')
        t1 = threading.Thread(target=workers, args=[tcpSerSock])
        t2 = threading.Thread(target=workers, args=[tcpSerSock])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        print(e)

    tcpSerSock.close()
