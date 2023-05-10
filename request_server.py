import socket
import json

player = ('0.0.0.0', 4000)
server = ('localhost', 3000) 

def sub():
    with socket.socket() as s: 
        try:
            s.connect(server)
            inscription = {
                "request": "subscribe",
                "port": player[1],
                "name": "Champions",
                "matricules": ["20089", "195105"]
            }
            s.send(json.dumps(inscription).encode())
            response = json.loads(s.recv(2048).decode())
            print(response)
        except OSError:
            print('Connexion failed')
            
        if response == {"response": "ok"}:
            print("Start the game!")
        else: 
            raise ValueError("Subscribing failed" + response)

        while True:
            try:
                data = s.recv(2048).decode()
                if data:
                    try:
                        request = json.loads(data)
                        if request["request"] == "ping":
                            s.send(json.dumps({"response": "pong"}).encode())
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON: {e}")
            except:
                break

sub()