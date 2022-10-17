import socket
import random
import ecdh

key_gen = ecdh.key()
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 4444))
sock.listen(0)
conn, addr = sock.accept()
client_half = conn.recv(1024)
conn.send(str(key_gen.half_key).encode())
full_key = key_gen.gen_full(int(client_half.decode()))

aes = ecdh.C2_AES(full_key)
conn.send(aes.encrypt("secret password"))