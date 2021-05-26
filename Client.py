import sys, socket, select, string, os

SIZE = 1024
ENCODING = 'utf-8'
MESSAGE_LENGTH_SIZE = 64


def get_host_port(arr):
    host = arr[1]
    port = int(arr[2])
    return host, port


def connect_to_remote_host(host, port):
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    created_socket.settimeout(1)

    try:
        created_socket.connect((host, port))
    except:
        print("Error: Unable to connect")
        sys.exit()

    res = "*** Connected to {} on port {} ***".format(host, port)
    print(res)

    return created_socket


def close_connection(socket):
    if socket:
        socket.close()


def send_message(client, message):
    message = message.encode()
    message_length = len(message)
    message_length = str(message_length).encode()
    message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))

    client.sendall(message_length)
    client.sendall(message)


def upload_file(client, path):
    # to prepare server for receive file,
    # client send message "upload" before upload file
    send_message(client, "upload")

    # send file name to server
    file_name = path.split('/')[-1]
    send_message(client, file_name)

    with open(path, 'rb') as file:
        payload_encode = file.read()
        payload_length = len(payload_encode)
        payload_length = str(payload_length).encode()
        payload_length += b' ' * (MESSAGE_LENGTH_SIZE - len(payload_length))

        client.sendall(payload_length)
        client.sendall(payload_encode)


def send_payload(client, payload_type, payload):
    if payload_type == "file":
        with open(payload, 'rb') as file:
            data = file.read()
            # while 1:
            #     data_in_chunk = file.read(SIZE)
            #     if not data_in_chunk:
            #         break
            #     send_payload(client, "data", data_in_chunk)
    else:
        print(111111111)
        client.sendall(payload.encode())
        # message = payload.encode()
        # message_length = len(message)
        # message_length = str(message_length).encode()
        # message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))
        #
        # print(message_length)
        # print(message)
        # client.sendall(message_length)
        # client.sendall(message)


def receive_data(socket):
    chunks_arr = bytearray()

    while 1:
        readable = select.select([socket], [], [], 2)
        if readable[0]:
            chunks_arr.extend(socket.recv(SIZE))
        else:
            break

    return chunks_arr.decode()


def receive_data2(connection):
    message_length = int(connection.recv(MESSAGE_LENGTH_SIZE).decode())
    message = connection.recv(message_length).decode()

    print("Client receive message from server.")
    return message


def network_scan(host, start_port, end_port):
    print(host)
    print(start_port, end_port)
    open_ports = []
    for port in range(start_port, end_port + 1):
        s = connect_to_remote_host(host, port)
        if s:
            print(port)
            open_ports.append("{}:{}".format(host, port))
            s.close()

    return open_ports


def exec_command_in_server(client, command):
    # to prepare server for execute command,
    # client send message "exec" before send command
    send_message(client, "exec")

    # send command to server
    send_message(client, command)



# for command "mkdir test1 test2"
# we have ["mkdir", "test1", "test2"]
# this function refactoring to "mkdir test1 test2"
def refactoring_command(arr):
    command = arr[2]
    for i in range(3, len(arr)):
        command += " " + arr[i]

    return command


if __name__ == "__main__":
    # print(network_scan("google.com", 80, 150))
    host, port = get_host_port(sys.argv)
    s = connect_to_remote_host(host, port)
    client_input = input()
    client_input_arr = client_input.split(" ")
    print(client_input_arr)

    if client_input_arr[0] == "telnet" and client_input_arr[1] == "upload":
        file_path = client_input_arr[2]
        upload_file(s, file_path)

    if client_input_arr[0] == "telnet" and client_input_arr[1] == "exec":
        command = refactoring_command(client_input_arr)
        print("*********************")
        print(command)
        exec_command_in_server(s, command)
        print(receive_data2(s))

    # exit()
    # print(command)
    # # command += "\n\n"
    # data = "GET / HTTP/1.1\r\nHost: google.com\n\n"
    # if data == command:
    #     print("the same")
    # send_payload(s, "other", command)
    # # send_payload(s, "orrr", "salam")
    # # send_payload(s, "orrr", "chetori!?")
    # # send_payload(s, "orrr", "DISCONNECT")
    # print(receive_data(s))
