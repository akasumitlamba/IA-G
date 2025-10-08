# aes_gcm.py
# AES-256-GCM encrypt/decrypt with password-derived key (PBKDF2-HMAC-SHA256)
# Usage:
#   Encrypt: python aes_gcm.py encrypt "Hello Wahyu" "my-strong-password"
#   Decrypt: python aes_gcm.py decrypt <b64_salt> <b64_nonce> <b64_ciphertext> "my-strong-password"

import os
import sys
import base64
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32         # 256-bit
PBKDF2_ITERS = 200_000

def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")

def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("utf-8"))

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive 256-bit key from password using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=PBKDF2_ITERS,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt(plaintext: str, password: str) -> Tuple[bytes, bytes, bytes]:
    """Returns (salt, nonce, ciphertext_with_tag)"""
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    # AESGCM.encrypt returns ciphertext || tag (tag is appended)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
    return salt, nonce, ct

def decrypt(salt: bytes, nonce: bytes, ct: bytes, password: str) -> str:
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, associated_data=None)
    return pt.decode("utf-8")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"encrypt", "decrypt"}:
        print("Usage:")
        print('  Encrypt: python aes_gcm.py encrypt "plaintext" "password"')
        print('  Decrypt: python aes_gcm.py decrypt <b64_salt> <b64_nonce> <b64_ciphertext> "password"')
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "encrypt":
        if len(sys.argv) != 4:
            print('Encrypt usage: python aes_gcm.py encrypt "plaintext" "password"')
            sys.exit(1)
        plaintext, password = sys.argv[2], sys.argv[3]
        salt, nonce, ct = encrypt(plaintext, password)
        print("SALT (b64):", b64e(salt))
        print("NONCE(b64):", b64e(nonce))
        print("CIPH(b64) :", b64e(ct))
        # Tip: store these three values together (salt, nonce, ciphertext)
    else:  # decrypt
        if len(sys.argv) != 6:
            print('Decrypt usage: python aes_gcm.py decrypt <b64_salt> <b64_nonce> <b64_ciphertext> "password"')
            sys.exit(1)
        salt_b64, nonce_b64, ct_b64, password = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        try:
            plaintext = decrypt(b64d(salt_b64), b64d(nonce_b64), b64d(ct_b64), password)
            print("PLAINTEXT:", plaintext)
        except Exception as e:
            # Auth failure (wrong password/salt/nonce/ct) will land here
            print("Decrypt failed:", str(e))
            sys.exit(2)

if __name__ == "__main__":
    main()
