import paho.mqtt.client as mqtt
import json

class PostoRecarga:
    def __init__(self, id, latitude, longitude, capacidade):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.capacidade = capacidade
        self.fila = []

        # Cria um cliente MQTT e configura as funções de callback
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso no broker MQTT.")
        client.subscribe("posto-recarga/{}/atualizar-fila".format(self.id))

    def on_message(self, client, userdata, msg):
        topic = msg.topic.split("/")
        if len(topic) == 4 and topic[3] == "atualizar-fila":
            self.enviar_fila()

    def enviar_fila(self):
        num_carros = len(self.fila)
        payload = {"num_carros": num_carros}
        self.client.publish("posto-recarga/{}/fila".format(self.id), json.dumps(payload), qos=1)

    def adicionar_carro(self):
        if len(self.fila) < self.capacidade:
            self.fila.append(1)
            print("Carro adicionado à fila do posto de recarga {}.".format(self.id))
        else:
            print("A fila do posto de recarga {} já está cheia.".format(self.id))

    def remover_carro(self):
        if len(self.fila) > 0:
            self.fila.pop(0)
            print("Carro removido da fila do posto de recarga {}.".format(self.id))
        else:
            print("A fila do posto de recarga {} está vazia.".format(self.id))

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()
