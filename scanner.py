import tkinter
# from tkinter import *
import socket
import threading
import queue
from IPy import IP

class Scanner(object):
    def __init__(self):
        # self.gi = pygeoip.GeoIP("./GeoLiteCity.dat")
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("Port-Scanner")

        # ip范围和端口范围，和需使用的线程数，显示结果
        self.ip_range_prompt = tkinter.Label(self.root,compound = 'left', fg = 'red',bg = '#FF00FF',text = 'ip range:')
        self.ip_range = tkinter.Entry(self.root)
        self.port_low_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'port_low:')
        self.port_low = tkinter.Entry(self.root)
        self.port_high_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'port_high:')
        self.port_high = tkinter.Entry(self.root)

        # thread num
        self.thread_num_prompt = tkinter.Label(self.root,fg = 'red',bg = '#FF00FF',text = 'thread num:')
        self.thread_num = tkinter.Entry(self.root)
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.scan, text = "Scan")

    def get_ip_status(self, ip, port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((ip,port))
            # server.open(ip,port)
            msg = '{0} port {1} is open'.format(ip, port)
            self.display_info.insert(tkinter.END,msg)
            print(msg)
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
        self.display_info.grid(columnspan=2, sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        self.result_button.grid(columnspan=2)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=5)
        self.root.rowconfigure(5, weight=1)

    def check(self):
        pass

    def check_open(self, q):
        try:
            while True:
                ip, port = q.get_nowait()
                self.get_ip_status(ip, port)
        except queue.Empty as e:
            # print("")
            pass

    def scan(self):
        self.check()
        self.display_info.delete(0, tkinter.END);
        ip_range = self.ip_range.get()
        start_port = int(self.port_low.get())
        end_port = int(self.port_high.get())
        thread_num = int(self.thread_num.get())

        # 生产者
        q = queue.Queue()
        hosts = IP(ip_range)
        for ip in hosts:
            for port in range(start_port, end_port):
                q.put((str(ip), port))
        # 消费者
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=self.check_open, args=(q,))
            t.start()
            threads.append(t)

        # for t in threads:
        #     t.join()


def main():
    # 初始化对象
    FL = Scanner()
    FL.gui_arrang()

    # 主程序执行
    FL.root.mainloop()


if __name__ == "__main__":
    main()
