import socketserver
import threading
from socket import *
from socketserver import *
import time
import cv2
import numpy


class MYRequestHandler(StreamRequestHandler):

    def handle(self) -> None:
        camera = cv2.VideoCapture("server/demo.mp4")
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]

        self.resolution = (640, 480)
        self.frame_len = b''
        self.frame_pyload = b''
        while True:
            self.data = self.request.recv(1024)
            if self.data:
                print("from {}".format(self.client_address), self.data)
                try:
                    _, self.img = camera.read()
                    self.img = cv2.resize(self.img, self.resolution)
                    _, img_encode = cv2.imencode('.jpg', self.img, img_param)
                    img_code = numpy.array(img_encode)
                    self.frame_pyload = img_code.tobytes()
                    self.frame_len = bytes(str(len(self.frame_pyload)).ljust(16), 'utf-8')
                    self.request.sendall(self.frame_len)
                    self.request.sendall(self.frame_pyload)
                    print(str(len(self.frame_pyload)).ljust(16))

                except Exception as e:
                    print("发送异常", e)
                    break
            else:
                break

        print("断开连接")
        self.request.close()


if __name__ == "__main__":
    addr = ("localhost", 123)
    server = ThreadingTCPServer(addr, MYRequestHandler)
    server.serve_forever()

    pass
