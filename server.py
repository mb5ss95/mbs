import socket 
import json
from _thread import *
import chardet


# 쓰레드에서 실행되는 코드입니다. 

# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
def threaded(client_socket, addr): 

    print('Connected by :', addr[0], ':', addr[1]) 



    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 
        # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
        data = client_socket.recv(1024)

        if not data: 
            print('Disconnected by ' + addr[0],':',addr[1])
            break
        print('Received from ' + addr[0],':',addr[1])
        print(chardet.detect(data)) # {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
        print(data)                  # b'\xac\xed\x00\x05'
            
        temp = data[3:].decode('utf-8')
        print('test' + temp)

             
    client_socket.close() 


HOST = '192.168.219.101'
PORT = 3000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')


# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 

    print('wait')


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 