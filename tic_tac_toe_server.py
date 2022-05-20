import socket

PORT = 8080

def main():
    server = socket.socket()
    server.bind(("", PORT))

    while True:
        server.listen(5)
        client, address = server.accept()
        print("{} connected".format(address))

        response = client.recv(255)
        if response != "":
            print(response)

if __name__ == '__main__':
    main()