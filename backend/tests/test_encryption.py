import pytest

from backend.utils.encryption import encrypt, decrypt

def test_roundtrip():
    # Encrypt then decrypt should return original value
    assert decrypt(encrypt("my-api-key")) == "my-api-key"

def test_encrypted_differs_from_plain():
    # Ciphertext must not equal plaintext
    assert encrypt("secret") != "secret"

def test_two_encryptions_differ():
    # Fernet uses random IV so same input yields different ciphertext
    assert encrypt("x") != encrypt("x")

def test_invalid_token_raises():
    # Decrypting garbage must raise an exception
    with pytest.raises(Exception):
        decrypt("not-a-valid-fernet-token")
