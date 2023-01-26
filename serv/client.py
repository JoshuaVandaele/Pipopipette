import socket
import argparse

def client(host: str = "127.0.0.1", port: int = 5000):
    print("Connecting to the server...")
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Done!")

    print("Waiting for the other player...")
    data = client_socket.recv(1).decode()
    if not data:
        print("The other player left!")
        client_socket.close()
        return
    if data == "time out":
        print("The other player took too long to join!")
        client_socket.close()
        return
    print("Done!")
    
    player = int(data)
    print(f"We are player {player}")
    
    while True: 
        try:
            if player == 1:
                message = input(" -> ")  # take input
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
                if data == "disconnect":
                    print("The other player left")
                    break
                if not data:
                    break
                print('Received from server: ' + data)
            else:
                data = client_socket.recv(1024).decode()
                if data == "disconnect":
                    print("The other player left")
                    break
                if not data:
                    break
                print('Received from server: ' + data)
                message = input(" -> ")  # take input
                client_socket.send(message.encode())
        except ConnectionResetError:
            print("Connection lost: An existing connection was forcibly closed by the remote host")
            break

    print("Disconnected from server")
    client_socket.close()  # close the connection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client')
    parser.add_argument('--port', '-p',
                        dest='tcp_port',
                        type=int,
                        choices=range(5000, 65536),
                        help='Listening TCP port',
                        default="5000")
    parser.add_argument('--host', '-H',
                        dest='host',
                        type=str,
                        help='Host address',
                        default="localhost")

    args = parser.parse_args()

    client(args.host, args.tcp_port)