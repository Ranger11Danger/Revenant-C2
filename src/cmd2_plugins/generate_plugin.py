from cmd2 import Cmd2ArgumentParser, with_argparser


generate_parser = Cmd2ArgumentParser()
generate_parser.add_argument("--ip", required=True, help="Port for implant to call back to")
generate_parser.add_argument("--port", required=True, help="port for implant to call back too")
generate_parser.add_argument("--format", required=True, choices=['python'], help="Payload code format")
generate_parser.add_argument("--name", required=True, help="Name for the output file")

class Plugin:
    @with_argparser(generate_parser)
    def do_generate_payload(self, args):
        self.do_run_pyscript(f"src/payload_templates/generate_python_payload.py --ip {args.ip} --port {args.port} --name {args.name}")
        print(f"Payload Saved to 'payloads/{args.name}'")