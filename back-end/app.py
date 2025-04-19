from flask_cors import CORS
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

CORS(app)
app = Flask(__name__)

# AES Encryption function
def encrypt_data(data, secret_key):
    """
    Encrypts the given data using AES encryption with the provided secret key.
    Returns the encrypted data in base64 format.
    """
    cipher = AES.new(secret_key, AES.MODE_EAX)  # EAX mode for authenticity and confidentiality
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    # Return a base64 encoded string combining nonce, tag, and ciphertext
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

# AES Decryption function
def decrypt_data(encrypted_data, secret_key):
    """
    Decrypts the given encrypted data using the provided secret key.
    Returns the decrypted string.
    """
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))  # Decode from base64
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode('utf-8')

# AES Secret key generation function
def generate_aes_key():
    """
    Generates a random 128-bit AES key.
    Returns a 16-byte key.
    """
    return get_random_bytes(16)  # AES-128 key

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """
    Encrypts the data sent via POST request and returns the encrypted data and key.
    The key is base64-encoded to be safely transmitted.
    """
    data = request.json.get('data')  # Get data from request
    if not data:
        return jsonify({'error': 'No data provided for encryption'}), 400  # Error if no data
    
    secret_key = generate_aes_key()  # Generate a random AES key
    encrypted_data = encrypt_data(data, secret_key)  # Encrypt the data
    # Return the encrypted data and the secret key in base64 encoding
    return jsonify({
        'encrypted_data': encrypted_data,
        'secret_key': base64.b64encode(secret_key).decode('utf-8')
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """
    Decrypts the encrypted data sent via POST request and returns the original data.
    """
    encrypted_data = request.json.get('encrypted_data')  # Get encrypted data from request
    secret_key = request.json.get('secret_key')  # Get secret key from request
    if not encrypted_data or not secret_key:
        return jsonify({'error': 'Encrypted data or secret key missing'}), 400  # Error if missing data
    
    secret_key = base64.b64decode(secret_key)  # Decode the base64 secret key
    try:
        decrypted_data = decrypt_data(encrypted_data, secret_key)  # Decrypt the data
        return jsonify({'decrypted_data': decrypted_data})  # Return the decrypted data
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Decryption failed'}), 400  # Handle decryption failures

if __name__ == "__main__":
    app.run(debug=True)
