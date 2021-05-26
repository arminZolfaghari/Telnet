SIZE = 1024
ENCODING = 'utf-8'
MESSAGE_LENGTH_SIZE = 64


def send_message(client, message):
    message = message.encode()
    message_length = len(message)
    message_length = str(message_length).encode()
    message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))

    client.sendall(message_length)
    client.sendall(message)