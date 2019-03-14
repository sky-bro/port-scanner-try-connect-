import tkinter
import socket

class Scanner(object):
    def __init__(self):
        # self.gi = pygeoip.GeoIP("./GeoLiteCity.dat")
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("Port-Scanner")

        # ip范围和端口范围，和需使用的线程数，显示结果
        self.ip_low = tkinter.Entry(self.root,width=30)
        self.ip_high = tkinter.Entry(self.root,width=30)
        self.port_low = tkinter.Entry(self.root,width=30)
        self.port_high = tkinter.Entry(self.root,width=30)

        # thread num
        self.thread_num = tkinter.Entry(self.root,width=30)
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root, width=50)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.scan, text = "Scan")

    def get_ip_status(self, ip, port_low, port_high):
        # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server = telnetlib.Telnet()
        for port in range(port_low, port_high+1):
            # print('current port', port)
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((ip,port))
                # server.open(ip,port)
                msg = '{0} port {1} is open'.format(ip, port)
                self.display_info.insert(0,msg)
                print(msg)
            except Exception as err:
                # print(err)
                # print('{0} port {1} is not open'.format(ip,port))
                pass
            finally:
                server.close()

    # 完成布局
    def gui_arrang(self):
        self.ip_low.pack()
        self.ip_high.pack()
        self.port_low.pack()
        self.port_high.pack()
        self.thread_num.pack()
        self.display_info.pack()
        self.result_button.pack()


    def scan(self):
        # ip_addr = self.ip_low.get()
        # start_port = int(self.port_low.get())
        # end_port = int(self.port_high.get())
        ip_addr = "127.0.0.1"
        start_port = 1
        end_port = 100
        self.get_ip_status(ip_addr, start_port, end_port)


def main():
    # 初始化对象
    FL = Scanner()
    FL.gui_arrang()

    # 主程序执行
    FL.root.mainloop()


if __name__ == "__main__":
    main()
