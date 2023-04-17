import socket
client = socket.socket()
#client.connect(('192.168.1.177',9999))
client.connect(('localhost',9000))
while True:
    msg = input(">>:").strip()
    if len(msg) == 0:continue
    client.send(msg.encode("utf-8"))
    data = client.recv(1024)
    print("recv:",data.decode())
client.close()