import sys, socket
from CommonFunctions import *

from Database import *

# for TLS connection
from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_CLIENT

SIZE = 4096
ENCODING = 'utf-8'
MESSAGE_LENGTH_SIZE = 64


def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        file_object.write("Time: {} -> client command: {}".format(current_time, text_to_append))


def read_history_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def print_history(readed_file):
    print("\n\n\n***** HISTOY *****")
    print(readed_file)
    print("******************\n\n\n")


def get_host_port(arr):
    host = arr[1]
    port = int(arr[2])
    return host, port


def connect_to_remote_host(host, port):
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # created_socket.settimeout(2)

    try:
        remote_ip = socket.gethostbyname(host)
        created_socket.connect((remote_ip, port))
        append_new_log_in_database("client", "start connection", "client connect to server.")
    except:
        print("Error: Unable to connect")
        sys.exit()

    res = "*** Connected to {} on port {} ***".format(host, port)
    print(res)

    return created_socket


def close_connection(socket):
    if socket:
        socket.close()


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
        append_new_log_in_database(client, "payload length (for upload file)", str(payload_length))
        client.sendall(payload_encode)
        append_new_log_in_database(client, "payload encode", str(payload_encode))

        # append_new_log_in_database("client", "client upload file", payload_encode)


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
    # append_new_log_in_database("client", "client send message 'exec' to server", "exec")

    # send command to server
    send_message(client, command)
    # append_new_log_in_database("client", "client send command to server", command)


# for command "mkdir test1 test2"
# we have ["mkdir", "test1", "test2"]
# this function refactoring to "mkdir test1 test2"
def rejoining_segment_of_array(arr, start, end):
    result = arr[start]
    for i in range(start + 1, end):
        result += " " + arr[i]

    return result


# def create_tls_socket(message):
#     ip = "1"
#     port = 8443
#     context = SSLContext(PROTOCOL_TLS_CLIENT)
#     context.load_verify_locations("./ssl-config/cert.pem")
#
#     with create_connection((ip, port)) as client:
#         with context.wrap_socket(client, server_hostname=hostname) as tls:
#
#             print(f'Using {tls.version()}\n')
#             tls.sendall(b'Hello, world')
#
#             data = tls.recv(1024)
#             print(f'Server says: {data}')


if __name__ == "__main__":
    # print(network_scan("google.com", 80, 150))
    host, port = get_host_port(sys.argv)
    s = connect_to_remote_host(host, port)
    exit_flag = False

    while not exit_flag:
        client_input = input()
        append_new_line("./history.txt", client_input)  # append in history file
        append_new_command_in_database(client_input)  # append in database
        client_input_arr = client_input.split(" ")

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "upload":
            file_path = client_input_arr[2]
            upload_file(s, file_path)

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "exec":
            command = rejoining_segment_of_array(client_input_arr, 2, len(client_input_arr))
            exec_command_in_server(s, command)
            print(receive_data(s))

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "send":
            message = rejoining_segment_of_array(client_input_arr, 2, len(client_input_arr))
            send_message(s, "send")
            send_message(s, message)

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "history":
            history = read_history_file("./history.txt")
            print_history(history)
            # print_history_from_database()

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "send" and client_input_arr[2] == "-e":
            message = rejoining_segment_of_array(client_input_arr, 3, len(client_input_arr))
            send_message(s, "-e")
            send_encrypted_message(s, message)

        if client_input_arr[0] == "telnet" and client_input_arr[1] == "exit":
            send_message(s, "exit")
            exit_flag = True
            close_connection(s)

        if client_input == "normal telnet":
            while True:
                request = input()
                request += "\r\n"
                s.send(request.encode())
                response = s.recv(SIZE)
                print(response.decode())
