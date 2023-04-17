from paho.mqtt import client as mqtt_client
import uuid
import time 
import random
from mqtt import Conectar_mqtt
broker = 'localhost'
port = 1883
topic = "URA001/teste"
client_id = f'python-mqtt-{random.randint(0, 100000000000)}'
print(client_id)

class PostoEnergia:
 
    def __init__(self):
        conectar = Conectar_mqtt
        self.client = conectar.connect_mqtt()
        self.publish()
        #self.client = self.connect_mqtt()
        #self.client.loop_start()
        #self.publish()
        

        #self.id  = f'python-mqtt-{random.randint(0, 1000)}'
        #self.regiao = regiao
        #self.lista = lista
        #self.client = cliente
        #pass

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("conectado ao MQTT!")
            else:
                print("Falha ao conectar, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        #client.publish(client)
        return client
         
    def verifi_connect_mqtt(client, userdata, flags, rc):
        if rc == 0:
            print("conectado ao MQTT!")
        else:
            print("Falha ao conectar, return code %d\n", rc)

    def atualizar_filas(self, filas):
        self.filas = filas

    def enviar_filas_mqtt(self, mensagem):
        broker = 'localhost'
        port = self.lista[self.regiao]
        topic = "enviar/fila"

    def simular(self, latitude_carro, longitude_carro):
        # simular o funcionamento do posto de energia
        pass

    def publish(self):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"counter: {msg_count}"
            result = self.client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1

def run():
    p = PostoEnergia()
  


if __name__ == '__main__':
    run()
