import { useState } from 'react';
import './App.css';

const API_URL = "http://127.0.0.1:5000"; // Update this when deploying

function App() {
  const [data, setData] = useState('');
  const [encryptedData, setEncryptedData] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const [decryptedData, setDecryptedData] = useState('');

  // Handle input change for encryption
  const handleDataChange = (e) => setData(e.target.value);

  // Handle encryption request
  const handleEncrypt = async () => {
    const response = await fetch(`${API_URL}/encrypt`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data }),
    });
    const result = await response.json();
    setEncryptedData(result.encrypted_data);
    setSecretKey(result.secret_key);
  };

  // Handle decryption request
  const handleDecrypt = async () => {
    const response = await fetch(`${API_URL}/decrypt`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        encrypted_data: encryptedData,
        secret_key: secretKey,
      }),
    });
    const result = await response.json();
    setDecryptedData(result.decrypted_data);
  };

  return (
    <div className="app-container">
      <h1>Quantum-Resistant Data Vault</h1>

      {/* Encryption Section */}
      <div className="form-container">
        <h2>Encryption</h2>
        <textarea
          placeholder="Enter data to encrypt"
          value={data}
          onChange={handleDataChange}
        />
        <button onClick={handleEncrypt}>Encrypt</button>
        {encryptedData && (
          <div className="output">
            <h3>Encrypted Data:</h3>
            <textarea value={encryptedData} readOnly />
            <h3>Secret Key:</h3>
            <textarea value={secretKey} readOnly />
          </div>
        )}
      </div>

      {/* Decryption Section */}
      <div className="form-container">
        <h2>Decryption</h2>
        <textarea
          placeholder="Enter encrypted data"
          value={encryptedData}
          onChange={(e) => setEncryptedData(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter secret key"
          value={secretKey}
          onChange={(e) => setSecretKey(e.target.value)}
        />
        <button onClick={handleDecrypt}>Decrypt</button>
        {decryptedData && (
          <div className="output">
            <h3>Decrypted Data:</h3>
            <textarea value={decryptedData} readOnly />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
