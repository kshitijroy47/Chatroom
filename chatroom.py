import socket
import threading
import rsa

host = '127.0.0.1'
port = 44444
pubkey,prikey = rsa.newkeys(1024)
pubpartner = None

clients = []
usernames = {}
pubkeys = {}

username = input("Enter your username: ")

choice = input("Press 1 if you want to host OR Press 2 if you want to connect to the chatroom:")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Launching Server...")
    
    client_socket, client_address = server.accept()
    client_socket.send(pubkey.save_pkcs1("PEM"))
    pubpartner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
    
    print(f"Connected with {client_address}")
    
    client_socket.send(username.encode())
    username = client_socket.recv(1024).decode()
    print(f"{username} joined the chatroom!")
    
elif choice == "2":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    pubpartner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
    client_socket.send(pubkey.save_pkcs1("PEM"))
    
    print("Connected to server.")
    
    partner_username = client_socket.recv(1024).decode()
    client_socket.send(username.encode())

else:
    exit()

def write():
    while True:
        message = input("")
        print("You: " + message)
        encrypted_message = rsa.encrypt((username + ": " + message).encode(), pubpartner)
        client_socket.send(encrypted_message)

def receive():
    while True:
        decrypted_message = rsa.decrypt(client_socket.recv(1024),prikey).decode()
        print(decrypted_message)

threading.Thread(target=write).start()
threading.Thread(target=receive).start()