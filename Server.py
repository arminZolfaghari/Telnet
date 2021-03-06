import socket, threading, subprocess
from CommonFunctions import *

PORT = 8877
SIZE = 1024
ENCODING = 'utf-8'
MESSAGE_LENGTH_SIZE = 64


def receive_file(connection, address):
    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    uploaded_file_name = connection.recv(message_length).decode()

    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    uploaded_file = connection.recv(message_length)

    path = "./server_file/" + uploaded_file_name
    new_file_in_server = open(path, "wb")
    new_file_in_server.write(uploaded_file)
    new_file_in_server.close()
    print("Server received file from {}".format(address))


# execute command and sends result to client
def exec_command(connection, address):
    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    command = connection.recv(message_length).decode()
    print(command, type(command))
    print("\n\n\n")

    result = subprocess.getoutput(command)
    print("result_encode {}".format(result))
    send_message(connection, result)  # server sends to client result of command
    print("Server execute command and sends result to client")


def handle_client(connection, address):
    print("[NEW CONNECTION] connected from {}".format(address))
    connection_status = True

    while connection_status:
        message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
        telnet_mode = connection.recv(message_length).decode()

        if telnet_mode == "upload":
            print("Client upload file, server is receiving ...")
            receive_file(connection, address)

        if telnet_mode == "exec":
            print("Client requested execute command ...")
            exec_command(connection, address)

        if telnet_mode == "send":
            print("Client send message to server")

        if telnet_mode == "-e":
            decrypt_message, encrypt_message = decrypted_message(connection)
            print("Client {} send message to server => message is encrypted: {}".format(address, encrypt_message))
            print("decrypted message is : {}".format(decrypt_message))

        if telnet_mode == "exit":
            connection_status = False
            # connection.close()

        # print("[MESSAGE RECEIVED] {}".format(message))
        #
        # if message == "DISCONNECT":
        #     connection_status = False


def start_server(server):
    print("server")
    print(server)
    server.listen()
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()


if __name__ == "__main__":
    address = socket.gethostbyname(socket.gethostname())
    host_information = (address, PORT)
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    created_socket.bind(host_information)
    print("[SERVER STARTS] Server is starting ...")
    start_server(created_socket)
