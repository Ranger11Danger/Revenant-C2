#!/bin/python3

from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser
from rich.console import Console
import json
import src.crypto.ecdh as ecdh

#import plugin files here
import src.cmd2_plugins.clients_plugin
import src.cmd2_plugins.connections_plugin
import src.cmd2_plugins.generate_plugin
import src.cmd2_plugins.commands_plugin
import src.cmd2_plugins.file_manage_plugin


class App(
        #We need to install the plugins here
        src.cmd2_plugins.clients_plugin.Plugin,
        src.cmd2_plugins.connections_plugin.Plugin, 
        src.cmd2_plugins.generate_plugin.Plugin,
        src.cmd2_plugins.commands_plugin.Plugin,
        src.cmd2_plugins.file_manage_plugin.Plugin,
        Cmd):

    console = Console()
    intro = "Welcome to the listener interface\nConnect to C2 server to start\n"
    prompt = "(Disconnected): "
    connection = {
    "socket" : None,
    "address" : None,
    "port" : None
    }
    clients = {}

    def negotiate_secret(self, conn):
        key_gen = ecdh.key()
        conn.send(str(key_gen.half_key).encode())
        client_half = conn.recv(1024)
        full_key = key_gen.gen_full(int(client_half.decode()))
        return full_key
    
    def encrypt_msg(self, msg, full_key):
        aes = ecdh.C2_AES(full_key)
        return aes.encrypt(msg)

    def decrypt_msg(self, encrypted_msg, full_key):
        aes = ecdh.C2_AES(full_key)
        return aes.decrypt(encrypted_msg)

     
app = App()
app.cmdloop()
