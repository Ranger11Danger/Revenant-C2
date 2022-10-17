use sodiumoxide::crypto::secretbox;

pub fn custom_decrypt(key: secretbox::Key, ciphertext: Vec<u8>) -> Vec<u8> {
    let nonce = secretbox::Nonce::from_slice(&ciphertext[..24]).unwrap();
    let their_plaintext= secretbox::open(&ciphertext[24..],&nonce , &key);
    their_plaintext.unwrap()
}

pub fn custom_encrypt(key: secretbox::Key, plaintext: String) -> (Vec<u8>, secretbox::Nonce) {
    let nonce = secretbox::gen_nonce();
    let ciphertext = secretbox::seal(plaintext.as_bytes(), &nonce, &key);
    (ciphertext, nonce)
}

