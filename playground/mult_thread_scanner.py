#!/usr/bin/env python

import socket
import telnetlib
import threading
import queue

def get_ip_status(ip):
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server = telnetlib.Telnet()
    for port in range(0,65536):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((ip,port))
            # server.open(ip,port)
            print('{0} port {1} is open'.format(ip, port))
        except Exception as err:
            # print(err)
            print('{0} port {1} is not open'.format(ip,port))
        finally:
            server.close()

def check_open(q):
    try:
        while True:
            ip = q.get_nowait()
            get_ip_status(ip)
    except queue.Empty as e:
        pass

if __name__ == '__main__':
    # host = ['10.0.0.10','10.0.0.11','10.0.0.12', '127.0.0.1']     # 这里模拟多IP地址的情况，也可以从文件中读取IP——list
    host = ['127.0.0.1']
    q = queue.Queue()
    for ip in host:
        q.put(ip)
    threads = []
    for i in range(10):
        t = threading.Thread(target=check_open,args=(q,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
