import socket
import json

HOST = 'localhost'
PORT = 3000  # Replace with the port number the server is listening on
NAME = 'Champions'
CLIENT_PORT = 5000  # This is the port the client will use for incoming connections
MATRICULES = ["20089", "195105"]

def handle_ping(conn):
    data = conn.recv(2048)
    request = json.loads(data.decode())
    if request['request'] == 'ping':
        response = json.dumps({'response': 'pong'}).encode()
        conn.send(response)
        conn.close()

def start_ping_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', CLIENT_PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                handle_ping(conn)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send subscription request
        request = {
            'request': 'subscribe',
            'name': NAME,
            'port': CLIENT_PORT,
            'matricules': MATRICULES,
        }
        s.send(json.dumps(request).encode())

        # Read the response
        data = s.recv(2048)
        response = json.loads(data.decode())
        print(response)

if __name__ == '__main__':
    main()

    try:
        start_ping_server()
    except KeyboardInterrupt:
        print("Shutting down the client")