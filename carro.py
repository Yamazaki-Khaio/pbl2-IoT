import paho.mqtt.client as mqtt
import json
import time

class Carro:
    def __init__(self, id, posto_recarga_id):
        self.id = id
        self.posto_recarga_id = posto_recarga_id

        # Cria um cliente MQTT e configura as funções de callback
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso no broker MQTT.")
        # Subscreve ao tópico da fila do posto de recarga
        client.subscribe("posto-recarga/{}/fila".format(self.posto_recarga_id))

    def solicitar_recarga(self):
        # Publica uma mensagem no tópico do posto de recarga
        payload = {"carro_id": self.id}
        self.client.publish("posto-recarga/{}/solicitar-recarga".format(self.posto_recarga_id), json.dumps(payload.encode("utf-8")), qos=1)

    def on_message(self, client, userdata, msg):
        topic = msg.topic.split("/")
        if len(topic) == 3 and topic[2] == "fila":
            # Recebe a mensagem com a fila atualizada
            payload = json.loads(msg.payload.decode("utf-8"))
            num_carros = payload["num_carros"]
            print("Carro {} está na posição {} da fila do posto de recarga {}.".format(self.id, num_carros, self.posto_recarga_id))

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()