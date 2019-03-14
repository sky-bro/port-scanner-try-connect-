import tkinter
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
        self.ip_range = tkinter.Entry(self.root,width=30)
        self.port_low = tkinter.Entry(self.root,width=30)
        self.port_high = tkinter.Entry(self.root,width=30)

        # thread num
        self.thread_num = tkinter.Entry(self.root,width=30)
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root, width=50)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.scan, text = "Scan")

    def get_ip_status(self, ip, port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((ip,port))
            # server.open(ip,port)
            msg = '{0} port {1} is open'.format(ip, port)
            self.display_info.insert(0,msg)
            print(msg)
        except Exception as err:
            # print(err)
            print('{0} port {1} is not open'.format(ip,port))
            pass
        finally:
            server.close()

    # 完成布局
    def gui_arrang(self):
        self.ip_range.pack()
        self.port_low.pack()
        self.port_high.pack()
        self.thread_num.pack()
        self.display_info.pack()
        self.result_button.pack()

    def check(self):
        pass

    def check_open(self, q):
        try:
            while True:
                ip, port = q.get_nowait()
                self.get_ip_status(ip, port)
        except queue.Empty as e:
            pass

    def scan(self):
        self.check()
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
