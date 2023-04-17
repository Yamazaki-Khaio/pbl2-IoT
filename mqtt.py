import random

broker = 'localhost'
port = 1883
topic = "URA001/teste"

from paho.mqtt import client as mqtt_client
class Conectar_mqtt:

    def connect_mqtt():
        
        client_id =  f'python-mqtt-{random.randint(0, 100000000000)}'
        try:
            client = mqtt_client.Client(client_id)
        except: 
           print("Não conectado " + client.id)
        client.connect(broker, port)
        return client
    