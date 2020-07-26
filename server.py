import socket 
import json
from _thread import *
import chardet


def threaded(client_socket, address): 

    print('C host :', address[0], ', port :', address[1]) 
    
    check = True

    while True: 

        receive_data = client_socket.recv(1024)

        if receive_data and check: 
            print('R host :', address[0], ', port :', address[1]) 
            #print(chardet.detect(receive_data))  # {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
            #print(receive_data)                  # b'\xac\xed\x00\x05'
            
            check = not check

            with open("C:/Users/mb5ss/Desktop/병짱맨/my_new.txt", "w") as json_file:
                json.dump(receive_data[3:].decode('utf-8'), json_file)

            

        else:
            print('D host :', address[0], ', port :', address[1]) 
            break

    client_socket.close()


HOST = '192.168.219.101'
PORT = 3000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')

while True: 

    print('wait')


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 