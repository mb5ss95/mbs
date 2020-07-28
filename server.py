import socket 
import json
import chardet
import numpy as np
from _thread import *
from PIL import Image

def image_to_data(image):
    """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
    # NumPy is much faster at doing this. NumPy code provided by:
    # Keith (https://www.blogger.com/profile/02555547344016007163)
    pb = np.array(image.convert('RGB')).astype('uint16')
    color = ((pb[:,:,0] & 0xF8) << 8) | ((pb[:,:,1] & 0xFC) << 3) | (pb[:,:,2] >> 3)
    return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()

def init_image(file_path):
    #이미지 파일 로드
    image = Image.open(file_path)
    #원하는 이미지 크기로 축소( 확대는 안됨 )
    #image.thumbnail((width, height), Image.ANTIALIAS)
    #image.thumbnail((width, height))

    #이미지 정사각형으로 변경
    #image = expand2square(image, backgroundColor)
    
    #이미지를 바이트 단위로 변경
    #pixelbytes = list(image_to_data(image))
    #temp = bytearray(list(image_to_data(image)))

    return bytes(list(image_to_data(image)))


def threaded(socket, address): 

    print('C0 host :', address[0], ', port :', address[1]) 
    

    while True: 
        receive_data = socket.recv(1024)[2:].decode('utf-8')
        if 'test' in receive_data:
            print('R1 host :', address[0], ', port :', address[1], ', data : ', receive_data) 
            file_path = 'F:/Other/사진/nako009.jpg'
            #gogo = init_image(file_path)

            with open(file_path, 'rb') as file:
                image_data = file.read()

            print('check please - ',   len(image_data))
            image_data = bytearray(image_data)
            socket.sendall (gogo)

            with open("C:/Users/mb5ss/Desktop/test/my_new.txt", "w") as json_file:
                json_file.write(str(gogo))
    
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
