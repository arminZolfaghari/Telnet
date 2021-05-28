from Database import *

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