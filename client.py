import time
from socket import *

import cv2
import numpy


def recv_all(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def test():
    host = socket()
    addr = ("localhost", 123)
    print("连接", addr)
    host.connect(addr)

    while True:
        host.send(bytes("i want a video", "utf-8"))
        try:
            tempdata_len = recv_all(host, 16)
            if tempdata_len is None:
                print("结束")
                break
            if len(tempdata_len) == 16:
                print("test", tempdata_len.decode())
                stringData = recv_all(host, int(tempdata_len.decode()))
                data = numpy.frombuffer(stringData, dtype="uint8")
                tmp = cv2.imdecode(data, 1)
                img = cv2.resize(tmp, (320, 240))
                cv2.imshow('Video', img)
                if cv2.waitKey(1) == 27:  # 按下ESC键
                    print("按下 Esc")
                    break
        except KeyboardInterrupt:
            print("Ctrl-C")
            break
        except Exception as e:
            print(e, "传输异常")
            break

    print("断开连接")
    host.close()
    print("关闭窗口")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test()
    pass
