from Database import *
from Crypthography import *

SIZE = 1024
ENCODING = 'utf-8'
MESSAGE_LENGTH_SIZE = 64


def send_message(sender, message):
    message = message.encode()
    message_length = len(message)
    message_length = str(message_length).encode()
    message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))

    sender.sendall(message_length)
    append_new_log_in_database(sender, "message length", str(message_length))
    sender.sendall(message)
    append_new_log_in_database(sender, "message", message)


def send_encrypted_message(sender, message):
    encrypted_encode_message = encrypt_message(message)
    message_length = len(encrypted_encode_message)
    message_length = str(message_length).encode()
    message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))

    sender.sendall(message_length)
    append_new_log_in_database(sender, "message length", str(message_length))
    sender.sendall(encrypted_encode_message)
    append_new_log_in_database(sender, "encrypted message", encrypted_encode_message)


def decrypted_message(connection):
    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    encrypted_message = connection.recv(message_length)
    origin_message = decrypt_message(encrypted_message)

    return origin_message, encrypted_message