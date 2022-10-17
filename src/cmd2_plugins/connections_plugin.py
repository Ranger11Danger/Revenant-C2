from cmd2 import Cmd2ArgumentParser, with_argparser
import socket
import threading

connect_argparser = Cmd2ArgumentParser()
connect_argparser.add_argument("--ip", required = True, help = "C2 address to connect to")
connect_argparser.add_argument("--port", help = "C2 port to connect to", default = 10000)
class Plugin:
    @with_argparser(connect_argparser)
    def do_connect(self, args):
        """
        connect to C2 Server
        """
        try:
            self.connection["socket"] = socket.create_connection((args.ip, args.port))
            self.connection["address"] = args.ip
            self.connection["port"] = args.port
            self.console.log(f"Connected to {args.ip}")
            self.c2_ip = args.ip
            self.prompt = f"(Connected): "
            self.aes_secret = self.negotiate_secret(self.connection["socket"])
            thread = threading.Thread(target=self.heartbeat, args=[])
            thread.daemon = True
            thread.start()
        except:
            self.console.log(f"Unable to connect to {args.ip}")

        
    
    def do_disconnect(self, args):
        self.prompt = "(Disconnected): "
        self.console.log(f"Disconnected from C2 at {self.connection['address']}:{self.connection['port']}")
        self.connection["socket"] = None