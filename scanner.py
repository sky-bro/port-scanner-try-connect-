import tkinter
# from tkinter import *
import socket
import threading
import queue
from IPy import IP
import time
import random
from concurrent.futures import ThreadPoolExecutor
import re

class Scanner(object):
    def __init__(self):
        # 生产者
        # self.q = queue.Queue()
        # self.emptyQ = threading.Event()
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("Port-Scanner")

        # ip范围和端口范围，和需使用的线程数，显示结果
        self.ip_range_prompt = tkinter.Label(self.root,compound = 'left', fg = 'red',bg = '#FF00FF',text = 'ip range:')
        ip_range = tkinter.StringVar()
        ip_range.set('127.0.0.1')
        self.ip_range = tkinter.Entry(self.root, textvariable=ip_range)
        self.port_low_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'port_low:')
        port_low = tkinter.StringVar()
        port_low.set('0')
        self.port_low = tkinter.Entry(self.root, textvariable=port_low)
        self.port_high_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'port_high:')
        port_high = tkinter.StringVar()
        port_high.set('65535')
        self.port_high = tkinter.Entry(self.root, textvariable=port_high)

        # thread num
        self.thread_num_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'thread num:')
        thread_num = tkinter.StringVar()
        thread_num.set('1')
        self.thread_num = tkinter.Entry(self.root, textvariable=thread_num)
        # 创建一个回显列表
        # self.display_info = tkinter.Listbox(self.root)
        self.text_result = tkinter.Text(self.root)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.scan, text = "Scan")

    def get_ip_status(self, ip_port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(1)
            server.connect(ip_port)
            # server.open(ip,port)
            msg = '{0} port {1} is open\n'.format(ip_port[0], ip_port[1])
            # self.display_info.insert(tkinter.END,msg)
            self.text_result.insert(tkinter.END, msg)
            print(msg, end='')
        except Exception as err:
            # print(err)
            # print('{0} port {1} is not open'.format(ip,port))
            pass
        finally:
            server.close()

    # 完成布局
    def gui_arrang(self):
        self.ip_range_prompt.grid(row=0,sticky=tkinter.E+tkinter.W)
        self.ip_range.grid(row=0,column=1, sticky=tkinter.E+tkinter.W)
        self.port_low_prompt.grid(row=1, sticky=tkinter.E+tkinter.W)
        self.port_low.grid(row=1,column=1, sticky=tkinter.E+tkinter.W)
        self.port_high_prompt.grid(row=2, sticky=tkinter.E+tkinter.W)
        self.port_high.grid(row=2,column=1, sticky=tkinter.E+tkinter.W)
        self.thread_num_prompt.grid(row=3,sticky=tkinter.E+tkinter.W)
        self.thread_num.grid(row=3,column=1, sticky=tkinter.E+tkinter.W)
        # self.display_info.grid(columnspan=2, sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
        self.text_result.grid(row=4, columnspan=2, sticky=tkinter.E+tkinter.W)

        self.result_button.grid(columnspan=2)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(4, weight=1)

    # def check(self):
    #     pass

    # def check_open(self):
    #     while True:
    #         try:
    #             ip, port = self.q.get_nowait()
    #             self.get_ip_status(ip, port)
    #         except queue.Empty as e:
    #             if self.emptyQ.is_set():
    #                 return
    #             time.sleep(random.random())
    #             print("empty")
    #             pass
    #
    # def producer(self, hosts, start_port, end_port):
    #     for ip in hosts:
    #         for port in range(start_port, end_port+1):
    #             self.q.put((str(ip), port))
    #     self.emptyQ.set()
    #
    # def consumer(self, thread_num):
    #     time_start=time.time()
    #     # 消费者
    #     threads = []
    #     for i in range(thread_num):
    #         t = threading.Thread(target=self.check_open)
    #         t.start()
    #         threads.append(t)
    #
    #     for t in threads:
    #         t.join()
    #     time_end=time.time()
    #     msg = '--'*5 + 'FINISH LINE' + '--'*5 + '\ntook {0} seconds'.format(time_end-time_start)
    #     # self.display_info.insert(tkinter.END,msg)
    #     self.text_result.insert(tkinter.END, msg)
    #     print(msg, end='')

    def scan(self):
        # self.check()
        # self.display_info.delete(0, tkinter.END);
        self.text_result.delete(0.0, tkinter.END);
        ip_range = self.ip_range.get()
        start_port = int(self.port_low.get())
        end_port = int(self.port_high.get())
        thread_num = int(self.thread_num.get())

        hosts = None
        try:
            hosts = IP(ip_range)
        except Exception as err:
            try:
                pattern = re.compile(r'(.*)-(.*)')
                m = pattern.match(ip_range)
                ip_low = IP(m.group(1)).int()
                ip_high = IP(m.group(2)).int()
                hosts = range(ip_low, ip_high+1)
            except Exception as ex:
                print(err)
                return

        def work():
            start_time = time.time()
            ex = ThreadPoolExecutor(thread_num)
            with ThreadPoolExecutor(thread_num) as ex:
                for host in hosts:
                    for port in range(start_port, end_port+1):
                        ex.submit(self.get_ip_status, (str(IP(host)), port))
            end_time = time.time()
            msg = '--'*5 + 'FINISH LINE' + '--'*5 + '\ntook {0} seconds\n'.format(end_time-start_time)
            # self.display_info.insert(tkinter.END,msg)
            self.text_result.insert(tkinter.END, msg)
            print(msg, end='')
        threading.Thread(target=work).start()

def main():
    # 初始化对象
    FL = Scanner()
    FL.gui_arrang()

    # 主程序执行
    FL.root.mainloop()


if __name__ == "__main__":
    main()
