import socket

HOST = '192.168.1.16'  # The server's hostname or IP address
PORT = 18000        # The port used by the server

def my_client():
    #threading.Timer(11, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        rec_length = 0
        expected = 27556
        data = ''
        while  expected - rec_length > 0:
            data += s.recv(expected - rec_length).decode('utf-8')
            rec_length = len(data)
        print(type(data))
        print(len(data))

        print(data)
        s.close()

    return data

if __name__ == "__main__":

    data = my_client()
    print(type(data))
    print(data)
    print(len(data))
