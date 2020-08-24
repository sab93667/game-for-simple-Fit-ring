import socket
import time
#Host = '192.168.137.1'
#Port = 5438

#s = socket.socket()
#s.bind((Host, Port))


#s.listen(5)
#print("server is running on {} with port {}".format(Host, Port))

def connect(host, port, listen_num):
    s = socket.socket()
    s.bind((host, port))
    #s.setblocking(False) 
    s.listen(listen_num)
    client, addr = s.accept()
    print('用戶端位址：{}，埠號：{}'.format(addr[0], addr[1]))
    return client

def get(client):
    try:        
        client.setblocking(0)
        msg = client.recv(1024).decode('utf8')
        return msg
    except:
        pass
    
'''    
while True:
    client, addr = s.accept()
    print("client's IP address: {}\nclient's port: {}".format(addr[0], addr[1]))
    while True:
        msg = client.recv(128).decode('utf-8')
        if msg == b'':
            print("something Wrong")
            break
        elif 'ok' in msg:
            print(msg[:-2])
            print("send 'received!'")
            client.send(b'received!')
        else:
            #print("message got from client:")
            print(msg,end='')
    #time.sleep(0.5)
    print("close connection!")
    client.close()
'''
#LAPTOP-20VNRJHU 