import socket
import json

addressplayer = ('0.0.0.0', 4000)

serveraddress = ('localhost', 10000) 

def subscribing ():
    with socket.socket() as s:
      client,adress =s.connect 
      try:
         s.connect(serveraddress)
         inscription = {
            "request": "subscribe",
            "port": addressplayer[1], #2e element de address player 
            "name": "Champion",
            "matricules": ["20089", "195105"]
         }
         s.send(json.dumps(inscription).encode()) #encode et converti inscription(python) en json 
         response = json.loads(s.recv(2048).decode()) #decode la reponse et convertis le fichier json 
         print(response)
