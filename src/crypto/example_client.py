import socket
import random
import ecdh

key_gen = ecdh.key()
sock = socket.create_connection(("127.0.0.1", 4444))
sock.send(str(key_gen.half_key).encode())
server_half = sock.recv(1024)
full_key = key_gen.gen_full(int(server_half.decode()))
encrypted_msg = sock.recv(1024)
aes = ecdh.C2_AES(full_key)
decrypted_msg = aes.decrypt(encrypted_msg)
print(encrypted_msg)
print(decrypted_msg)