"""
MAIN BASE FOUNDATION
Secure Vault — Encryption Boundary

This module provides the encryption boundary for the
Secure Vault.

Rules:

- Plaintext secrets must never be persisted.
- Encryption keys must not be stored with encrypted data.
- Encryption/decryption must happen only through this layer.
- The vault model stores ciphertext, not plaintext.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from typing import Optional


# =========================================================
# 🔐 ENCRYPTION CONFIGURATION
# =========================================================

_ENCRYPTION_VERSION = "1"
_NONCE_SIZE = 16
_SALT_SIZE = 16


# =========================================================
# 🔑 KEY DERIVATION
# =========================================================

def derive_key(
    master_key: str,
    salt: bytes,
) -> bytes:
    """
    Derive a fixed-length encryption key from a master key.

    The master key itself is never persisted by this module.
    """

    if not isinstance(master_key, str):
        raise TypeError(
            "Master key must be a string."
        )

    if not master_key.strip():
        raise ValueError(
            "Master key cannot be empty."
        )

    if not isinstance(salt, bytes):
        raise TypeError(
            "Salt must be bytes."
        )

    if not salt:
        raise ValueError(
            "Salt cannot be empty."
        )

    return hashlib.pbkdf2_hmac(
        "sha256",
        master_key.encode("utf-8"),
        salt,
        600_000,
        dklen=32,
    )


# =========================================================
# 🧱 STREAM KEY MATERIAL
# =========================================================

def _derive_keystream(
    key: bytes,
    nonce: bytes,
    length: int,
) -> bytes:
    """
    Generate deterministic key material for the requested
    ciphertext length.

    This is an internal primitive only.
    """

    if length < 0:
        raise ValueError(
            "Length cannot be negative."
        )

    output = bytearray()
    counter = 0

    while len(output) < length:

        block = hashlib.sha256(
            key
            + nonce
            + counter.to_bytes(
                8,
                "big",
            )
        ).digest()

        output.extend(block)
        counter += 1

    return bytes(
        output[:length]
    )


# =========================================================
# 🔒 INTERNAL ENCRYPTION
# =========================================================

def _encrypt_bytes(
    plaintext: bytes,
    key: bytes,
) -> bytes:
    """
    Encrypt bytes using authenticated ciphertext format.

    The returned value contains:

        version
        salt
        nonce
        ciphertext
        authentication tag
    """

    if not isinstance(
        plaintext,
        bytes,
    ):
        raise TypeError(
            "Plaintext must be bytes."
        )

    if not isinstance(
        key,
        bytes,
    ):
        raise TypeError(
            "Encryption key must be bytes."
        )

    if not key:
        raise ValueError(
            "Encryption key cannot be empty."
        )

    salt = os.urandom(
        _SALT_SIZE
    )

    nonce = os.urandom(
        _NONCE_SIZE
    )

    # Derive encryption material from supplied key
    derived = hashlib.sha256(
        key + salt
    ).digest()

    keystream = _derive_keystream(
        derived,
        nonce,
        len(plaintext),
    )

    ciphertext = bytes(
        value ^ stream
        for value, stream
        in zip(
            plaintext,
            keystream,
        )
    )

    header = (
        _ENCRYPTION_VERSION.encode(
            "ascii"
        )
        + b":"
        + salt
        + nonce
    )

    tag = hmac.new(
        derived,
        header + ciphertext,
        hashlib.sha256,
    ).digest()

    return (
        header
        + ciphertext
        + tag
    )


# =========================================================
# 🔓 INTERNAL DECRYPTION
# =========================================================

def _decrypt_bytes(
    encrypted: bytes,
    key: bytes,
) -> bytes:
    """
    Decrypt and authenticate ciphertext.
    """

    if not isinstance(
        encrypted,
        bytes,
    ):
        raise TypeError(
            "Encrypted data must be bytes."
        )

    if not isinstance(
        key,
        bytes,
    ):
        raise TypeError(
            "Encryption key must be bytes."
        )

    minimum_size = (
        2
        + _SALT_SIZE
        + _NONCE_SIZE
        + 32
    )

    if len(encrypted) < minimum_size:
        raise ValueError(
            "Invalid encrypted payload."
        )

    separator = encrypted.find(
        b":"
    )

    if separator <= 0:
        raise ValueError(
            "Invalid encryption header."
        )

    version = encrypted[
        :separator
    ].decode(
        "ascii"
    )

    if version != _ENCRYPTION_VERSION:
        raise ValueError(
            "Unsupported encryption version."
        )

    position = separator + 1

    salt = encrypted[
        position:
        position + _SALT_SIZE
    ]

    position += _SALT_SIZE

    nonce = encrypted[
        position:
        position + _NONCE_SIZE
    ]

    position += _NONCE_SIZE

    if len(encrypted) < position + 32:
        raise ValueError(
            "Invalid encrypted payload."
        )

    ciphertext = encrypted[
        position:-32
    ]

    stored_tag = encrypted[
        -32:
    ]

    derived = hashlib.sha256(
        key + salt
    ).digest()

    header = (
        encrypted[
            :position
        ]
    )

    expected_tag = hmac.new(
        derived,
        header + ciphertext,
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(
        stored_tag,
        expected_tag,
    ):
        raise ValueError(
            "Encrypted payload authentication failed."
        )

    keystream = _derive_keystream(
        derived,
        nonce,
        len(ciphertext),
    )

    return bytes(
        value ^ stream
        for value, stream
        in zip(
            ciphertext,
            keystream,
        )
    )


# =========================================================
# 🔐 PUBLIC ENCRYPTION API
# =========================================================

def encrypt_secret(
    secret: str,
    master_key: str,
) -> str:
    """
    Encrypt a secret and return an encoded ciphertext.

    The returned string is safe to place in the vault model
    as encrypted_password / encrypted_content.
    """

    if not isinstance(
        secret,
        str,
    ):
        raise TypeError(
            "Secret must be a string."
        )

    if not secret:
        raise ValueError(
            "Secret cannot be empty."
        )

    if not isinstance(
        master_key,
        str,
    ):
        raise TypeError(
            "Master key must be a string."
        )

    key_salt = hashlib.sha256(
        master_key.encode(
            "utf-8"
        )
    ).digest()

    key = derive_key(
        master_key,
        key_salt,
    )

    encrypted = _encrypt_bytes(
        secret.encode("utf-8"),
        key,
    )

    return base64.urlsafe_b64encode(
        encrypted
    ).decode(
        "ascii"
    )


# =========================================================
# 🔓 PUBLIC DECRYPTION API
# =========================================================

def decrypt_secret(
    encrypted_secret: str,
    master_key: str,
) -> str:
    """
    Decrypt a previously encrypted secret.

    Incorrect keys or tampered ciphertext are rejected.
    """

    if not isinstance(
        encrypted_secret,
        str,
    ):
        raise TypeError(
            "Encrypted secret must be a string."
        )

    if not encrypted_secret:
        raise ValueError(
            "Encrypted secret cannot be empty."
        )

    if not isinstance(
        master_key,
        str,
    ):
        raise TypeError(
            "Master key must be a string."
        )

    try:

        encrypted = (
            base64.urlsafe_b64decode(
                encrypted_secret.encode(
                    "ascii"
                )
            )
        )

    except Exception as exc:

        raise ValueError(
            "Invalid encrypted secret encoding."
        ) from exc

    key_salt = hashlib.sha256(
        master_key.encode(
            "utf-8"
        )
    ).digest()

    key = derive_key(
        master_key,
        key_salt,
    )

    plaintext = _decrypt_bytes(
        encrypted,
        key,
    )

    return plaintext.decode(
        "utf-8"
    )


# =========================================================
# 🧪 ENCRYPTION TEST
# =========================================================

def verify_encryption(
    secret: str,
    master_key: str,
) -> bool:
    """
    Verify that a secret can be encrypted and restored.

    This is intended for controlled testing.
    """

    encrypted = encrypt_secret(
        secret,
        master_key,
    )

    restored = decrypt_secret(
        encrypted,
        master_key,
    )

    return hmac.compare_digest(
        secret,
        restored,
    )


# =========================================================
# 📊 ENCRYPTION STATUS
# =========================================================

def encryption_status() -> dict:
    """
    Return encryption subsystem metadata.
    """

    return {
        "service": "secure_vault_encryption",
        "version": _ENCRYPTION_VERSION,
        "plaintext_persistence": False,
        "authenticated_ciphertext": True,
        "key_derivation": "PBKDF2-HMAC-SHA256",
    }


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [
    "derive_key",
    "encrypt_secret",
    "decrypt_secret",
    "verify_encryption",
    "encryption_status",
]
