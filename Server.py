import sys, socket, select, string, os, threading, subprocess

PORT = 8877
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


def exec_command(connection, address):
    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    command = connection.recv(message_length).decode()
    print(command, type(command))

    result = subprocess.getoutput(command)




def handle_client(connection, address):
    print("[NEW CONNECTION] connected from {}".format(address))
    connection_status = True

    while connection_status:
        message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
        telnet_mode = connection.recv(message_length).decode()

        if telnet_mode == "upload":
            print("Client upload file, server is receiving ...")
            receive_file(connection, address)
        elif telnet_mode == "exec":
            print("Client requested execute command")
            exec_command(connection, address)


        # print("[MESSAGE RECEIVED] {}".format(message))
        #
        # if message == "DISCONNECT":
        #     connection_status = False

    connection.close()


def start_server(server):
    print("server")
    print(server)
    server.listen()
    while True:
        connection, address = server.accept()
        print("connection server.accept")
        print(connection)
        print(address)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()


if __name__ == "__main__":
    address = socket.gethostbyname(socket.gethostname())
    host_information = (address, PORT)
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    created_socket.bind(host_information)
    print("[SERVER STARTS] Server is starting ...")
    start_server(created_socket)
