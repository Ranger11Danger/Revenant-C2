use tokio::{net::TcpSocket, io::{AsyncWriteExt, AsyncReadExt},net::TcpStream};
use serde::{Serialize, Deserialize};
use sodiumoxide::crypto::secretbox;
use std::io;
use rand::{Rng, rngs::ThreadRng};
use gethostname::gethostname;
use crypto::digest::Digest;
use crypto::sha2::Sha256;

pub fn gen_key(x:i128,y:u32, z :i128) -> i128{
    x.pow(y) % z
}
#[derive(Serialize, Deserialize, Debug)]
pub struct IntroMsg {
    pub hostname: String,
    pub date: String,
    pub time: String,
    pub number: String
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Payload {
    pub client_id : String,
    pub command : String,
    pub data : String
}

pub async fn recv_data(stream: &mut TcpStream) -> Vec<u8>{
    let mut data: Vec<u8> = vec![0;16];
    stream.read(&mut data).await.unwrap();
    let data_len: i32 = std::str::from_utf8(&data).unwrap().parse::<i32>().unwrap();
    let mut buff: Vec<u8> = vec![0;data_len.try_into().unwrap()];
    stream.read(&mut buff).await.unwrap();
    buff
}


pub async fn intro(sock: &mut TcpStream) -> io::Result<secretbox::Key> {
    let mut rng: ThreadRng = rand::thread_rng();
    let secret: u32 = rng.gen_range(1..10);
    let msg: IntroMsg = IntroMsg{
        hostname : gethostname().into_string().unwrap(),
        date : chrono::Utc::now().date().to_string(),
        time : chrono::Utc::now().time().to_string(),
        number: gen_key(6,secret,991).to_string()
    };
    sock.write_all(serde_json::to_string(&msg).unwrap().as_bytes()).await?;
    let mut data: Vec<u8> = vec![0;1024];
    sock.read(&mut data).await.unwrap();
    let shared: i128 = std::str::from_utf8(&data).unwrap().split("\0").collect::<Vec<&str>>()[0].parse::<i128>().unwrap();
    let final_num: i128 = gen_key(shared, secret, 991);
    let mut hasher: Sha256 = Sha256::new();
    hasher.input_str(&final_num.to_string());
    let key: secretbox::Key  = secretbox::Key::from_slice(&hasher.result_str()[..32].as_bytes()).unwrap();
    
    Ok(key)
}