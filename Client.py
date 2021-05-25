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


def send_payload(client, payload_type, payload):
    if payload_type == "file":
        with open(payload, 'rb') as file:
            while 1:
                data_in_chunk = file.read(SIZE)
                if not data_in_chunk:
                    break
                send_payload(client, "data", data_in_chunk)
    else:
        print(111111111)
        client.sendall(payload.encode())
        # message = payload.encode(ENCODING)
        # message_length = len(message)
        # message_length = str(message_length).encode(ENCODING)
        # message_length += b' ' * (MESSAGE_LENGTH_SIZE - len(message_length))
        #
        # print(message_length)
        # print(message)
        # client.send(message_length)
        # client.send(message)


def receive_data(socket):
    chunks_arr = bytearray()

    while 1:
        readable = select.select([socket], [], [], 2)
        if readable[0]:
            chunks_arr.extend(socket.recv(SIZE))
        else:
            break

    return chunks_arr.decode()


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

# def message(socket):
#     while 1:
#         socket_list = [sys.stdin, socket]
#         # Get the list sockets which are readable
#         read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
#
#         for sock in read_sockets:
#             # incoming message from remote server
#             if sock == socket:
#                 data = sock.recv(4096)
#                 if not data:
#                     print('Connection closed')
#                     sys.exit()
#                 else:
#                     # print data
#                     sys.stdout.write(data)
#
#             # user entered a message
#             else:
#                 msg = sys.stdin.readline()
#                 socket.send(msg)


if __name__ == "__main__":
    # print(network_scan("google.com", 80, 150))
    host, port = get_host_port(sys.argv)

    s = connect_to_remote_host(host, port)
    command = input()
    print(command)
    command += "\n\n"
    data = "GET / HTTP/1.1\nHost: google.com\n\n"
    if data == str(command):
        print("the same")
    send_payload(s, "orrr", command)
    print(receive_data(s))
