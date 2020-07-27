import socket 
import json
import chardet


def threaded(socket, address): 

    print('C0 host :', address[0], ', port :', address[1]) 
    

    while True: 
        receive_data = socket.recv(1024)[2:].decode('utf-8')
        if 'test' in receive_data:
            print('R1 host :', address[0], ', port :', address[1], ', data : ', receive_data) 
            file_path = 'F:/Other/사진/nako009.jpg'
            gogo = init_image(file_path)
            with open("C:/Users/mb5ss/Desktop/test/my_new.txt", "w") as json_file:
                json_file.write(str(gogo))
            socket.sendall (gogo)
            print('success')

        elif 'real' in receive_data: 
            print('R2 host :', address[0], ', port :', address[1], ', data : ', receive_data) 
            #print(chardet.detect(receive_data))  # {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
            #print(receive_data)                  # b'\xac\xed\x00\x05'

            with open("C:/Users/mb5ss/Desktop/test/my_new.txt", "w") as json_file:
                json.dump(receive_data, json_file)

        elif not receive_data:
            print('D0 host :', address[0], ', port :', address[1]) 
            break
    
    
    socket.close()


HOST = '192.168.219.101'
PORT = 3000
file_path = 'F:/Other/사진/nako009.jpg'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')

while True: 

    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 
