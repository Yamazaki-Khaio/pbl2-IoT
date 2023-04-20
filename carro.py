import paho.mqtt.client as mqtt
import time
import random

class CarroEletrico:

    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.carga_atual = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso no broker MQTT.")
        client.subscribe("carro-eletrico/" + str(self.id) + "/status")

    def enviar_status(self):
        status = {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "carga_atual": self.carga_atual
        }

        self.client.publish("carro-eletrico/" + str(self.id) + "/status", str(status))
        print("Enviando status do carro elétrico " + str(self.id) + ": " + str(status))

    def descarregar_bateria(self):
        descarga = random.choice(["lenta", "rápida", "média"])
        if descarga == "lenta":
            carga_perdida = random.randint(1, 5)
        elif descarga == "rápida":
            carga_perdida = random.randint(6, 10)
        else:
            carga_perdida = random.randint(11, 15)

        self.carga_atual -= carga_perdida
        print("Descarregando bateria do carro elétrico " + str(self.id) + " em " + str(carga_perdida) + " unidades.")
