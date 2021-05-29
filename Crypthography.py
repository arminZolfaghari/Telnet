from cryptography.fernet import Fernet

KEY = b'5QFu_jWQsqlT802ksnAs2F6j7fMjZ0xyLhuFvL4xswE='


def encrypt_message(message):
    fernet = Fernet(KEY)
    print(fernet)
    encMessage = fernet.encrypt(message.encode())

    return encMessage


def decrypt_message(enc_message):
    fernet = Fernet(KEY)

    decMessage = fernet.decrypt(enc_message).decode()

    return decMessage

