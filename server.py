import select
import socket
import queue

server = socket.socket()
server.bind(('localhost' ,9000))
server.listen(1000)

# 设置非阻塞模式
server.setblocking(False)
msg_dic = {}

# 内核检测并发链接
inputs = [server,]

# outputs存放链接需要返回的数据
outputs = []

# 为了循环调入select加入while
while True:

    # 1,需要内核检测哪些链接，有一个活动就返回所有链接循环。
    # 2,处理返回数据。
    # 3,如果有并发的链接断开，内核会返回报错到inputs内，有哪几个有问题。
    # 有链接进入会返回三个数据：
    # readable：返回一个列表，活动的，可读数据的
    # writeable：存放需要返回的数据。
    # exceptional：返回出现异常的活动链接
    readable,writeables,exceptional = select.select(inputs,outputs,inputs)
    print(readable,writeables,exceptional)

    # 收处理
    for r in readable:
        # 代表来了一个新连接
        if r is server:

            # 等待客户端生成实例
            conn,addr = server.accept()

            # 打印客户端IP地址
            print("来了个新连接",addr)

            #   因为这个新建里的链接还没发数据过来，现在就收数据的话程序就报错了
            #所以要想实现客户端发数据来时server端能知道，就需要让select在检测这
            #个conn。
            inputs.append(conn)

            # 初始化一个队列，后面存要返回这个客户端的数据
            msg_dic[conn] = queue.Queue()

        # 接收新连接数据
        else:
            # 获取数据
            data = r.recv(1024)
            # 打印数据
            print("收到数据:",data)

            # 将返回的数据排列到队列中
            msg_dic[r].put(data)

            # 放入返回的链接队列
            outputs.append(r)

    # 发数据：要返回给客户端的链接列表
    for w in writeables:
        # 重链接列表中取出队列的实例
        data_to_client = msg_dic[w].get()
        # 返回给客户端数据
        w.send(data_to_client)
        # 确保下次循环的时候writeable，不返回这个已经处理完的链接
        outputs.remove(w)

    # 删除：错误链接
    for e in exceptional:
        # 查找错误链接是否存在outputs
        if e in outputs:
            # 如果有就删除错误链接
            outputs.remove(e)
        # 删除inputs下的错误链接
        inputs.remove(e)
        # 删除队列中的错误链接
        del msg_dic[e]