import socket
import argparse 

# Timeout for two players to join before the connection is dropped
CONNECTION_TIMEOUT = 30

def server(host: str = "127.0.0.1", port: int = 5000):

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    print(f"\n-=== Listening for connections on {host}:{port} ===-")

    print("Waiting for player 1 to join...")
    conn1, address1 = server_socket.accept()  # accept new connection
    print(f"Connection from {address1}")

    server_socket.settimeout(CONNECTION_TIMEOUT)
        
    try:
        print("Waiting for player 2 to join...")
        conn2, address2 = server_socket.accept()  # accept new connection
        print(f"Connection from {address2}")
    except TimeoutError:
        print("Timed out: Waiting time exceeded")
        conn1.send("time out".encode())
        conn1.close()
        return
    
    server_socket.settimeout(None)

    conn1.send("1".encode())  # Tell the client they are player 1
    conn2.send("2".encode())  # Tell the client they are player 2
    print(f"OK! Player 1 is {address1} and Player 2 is {address2}")

    while True:
        try:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn1.recv(1024).decode()
            if not data:
                conn2.send("disconnect".encode())  # send data to the client
                print("Player 1 disconnected")
                break
            print("from p1: " + str(data))
            conn2.send(data.encode())  # send data to the client
            data = conn2.recv(1024).decode()
            if not data:
                conn1.send("disconnect".encode())  # send data to the client
                print("Player 2 disconnected")
                break
            print("from p2: " + str(data))
            conn1.send(data.encode())  # send data to the client
        except ConnectionResetError:
            print("Connection lost: An existing connection was forcibly closed by the remote host")
            break
    print("Dropped clients")
    conn1.close()  # close the connection
    conn2.close()  # close the connection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game server')
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
    while True:
        server(args.host, args.tcp_port)