from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

keys_directory = Path("secrets")
private_key_patch = keys_directory / "jwt_private.pem"
public_key_patch = keys_directory / "jwt_public.pem"

if private_key_patch.exists() or public_key_patch.exists():
    raise FileExistsError(
        "JWT keys alredy exist."
        "Remove them explicitly if rotation is intended."
    )

keys_directory.mkdir(
    parents=True,
    exist_ok=True,
)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

private_key_patch.write_bytes(
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
)

public_key_patch.write_bytes(
    private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
)

print(f"Private key: {private_key_patch}")
print(f"Public key: {public_key_patch}")