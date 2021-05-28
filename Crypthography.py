from cryptography.fernet import Fernet

KEY = b'5QFu_jWQsqlT802ksnAs2F6j7fMjZ0xyLhuFvL4xswE='


def encrypt_message(message):
    fernet = Fernet(KEY)
    print(fernet)
    encMessage = fernet.encrypt(message.encode())
    print(encMessage)

    return encMessage


def decrypt_message(enc_message):
    fernet = Fernet(KEY)
    print(fernet)
    decMessage = fernet.decrypt(enc_message).decode()
    print(decMessage)

    return decMessage


# a = encrypt_message("aloooo")
#
# print("*********************")
#
# # decrypt_message()
#
# decrypt_message(a)
