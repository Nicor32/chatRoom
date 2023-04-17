import socket


class Client:
    def __init__(self, host, port):
        self.client = socket.socket()
        # client.connect(('192.168.1.177',9999))
        self.client.connect((host, port))

    def run(self):
        while True:
            # msg = input(">>:").strip()
            # if len(msg) == 0: continue
            # self.client.send(msg.encode("utf-8"))
            data = self.client.recv(1024)
            if len(data) == 0: continue
            print("recv:", data.decode())
        # self.client.close()

    def send(self, buffer):
        msg = input(">>:").strip()
        if len(msg) != 0:
            self.client.send(msg.encode("utf-8"))


if __name__ == '__main__':
    client = Client('localhost', 8888)
    client.run()