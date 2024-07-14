import socket
import threading
import random
import math

def is_prime (number):
    if number < 2:
        return False
    for i in range (2, number // 2 +1):
        if number % i == 0:
            return False
    return True

def generate_prime (min_value, max_value):
    prime = random.randint (min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi):
    for d in range (3, phi):
        if (d * e) % phi == 1:
            return d 
    raise ValueError ("Mod_inverse does not exist!")

p, q = generate_prime(5, 210), generate_prime (5, 210)

while p==q:
    q= generate_prime(5, 210)

n = p * q
phi_n = (p-1) * (q-1)

e = random.randint (3, phi_n-1)
while math.gcd(e, phi_n) != 1: 
     e = random.randint (3, phi_n - 1)

d = mod_inverse(e, phi_n)

host = '127.0.0.1'
port = 44444

choice = input("Press 1 if you want to host OR Press 2 if you want to connect to the chatroom:")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Launching Server...")
    client_socket, client_address = server.accept()
    print(f"Connected with {client_address}")
    
elif choice == "2":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server.")

else:
    exit()

def write():
    while True:
        message = input("")
        print("You: " + message)
        message_encoded = [ord(ch) for ch in message]
        ciphertext = [pow(ch, e, n) for ch in message_encoded]
        client_socket.send(str(ciphertext).encode())

def receive():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            ciphertext = eval(data)
            Decodemsg= [pow(ch, d, n) for ch in ciphertext] 
            decrypted_message = "".join (chr(ch) for ch in Decodemsg)
            print(f"Partner: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break

# Start write and receive threads
threading.Thread(target=write).start()
threading.Thread(target=receive).start()
