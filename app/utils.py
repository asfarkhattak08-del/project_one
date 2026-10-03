from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def verify(plain_password, hashed_password):
    confrim = password_hash.verify(plain_password, hashed_password)
    return str(confrim)