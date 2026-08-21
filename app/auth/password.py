from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

DUMMY_PASSWORD_HASH = password_hash.hash(
    "dummy-password-that-is-never-used"
)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
        password: str,
        hashed_password: str
) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )