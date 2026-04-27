"""Password hashing and verification.

Uses ``pbkdf2_hmac`` from the Python standard library so the template has
zero password-related external dependencies. Replace with a stronger
algorithm (argon2 / bcrypt) in your application if needed — keep
``hash_password`` / ``verify_password`` as the public surface.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets


_PBKDF2_ITER = 240_000
_PBKDF2_ALGO = "sha256"


def hash_password(password: str) -> str:
    """Return a hashed representation of *password*."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        _PBKDF2_ALGO, password.encode("utf-8"), salt, _PBKDF2_ITER
    )
    return f"pbkdf2${_PBKDF2_ALGO}${_PBKDF2_ITER}${salt.hex()}${digest.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify *password* against *hashed*. Constant-time compare."""
    if not hashed.startswith("pbkdf2$"):
        return False
    try:
        _, algo, iters, salt_hex, digest_hex = hashed.split("$")
        digest = hashlib.pbkdf2_hmac(
            algo, password.encode("utf-8"), bytes.fromhex(salt_hex), int(iters)
        )
    except Exception:
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


def generate_secret(nbytes: int = 32) -> str:
    """Helper to generate a cryptographically strong secret."""
    return secrets.token_urlsafe(nbytes)
