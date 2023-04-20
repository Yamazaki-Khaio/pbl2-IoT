import requests
import random
import json
import paho.mqtt.client as mqtt
import time

# Configurações do servidor REST
REST_API_URL = "http://posto-api:5000"
REST_API_ROTA_BUSCA_POSTO = "/postos/busca"
REST_API_ROTA_ABASTECE_POSTO = "/postos/abastece"

# Configurações do broker MQTT
MQTT_BROKER = "posto-mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "posto"

class ComputadorDeBordo:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.client_mqtt = mqtt.Client()
        self.client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client_mqtt.loop_start()

    def buscar_posto_mais_proximo(self):
        response = requests.get(f"{REST_API_URL}/postos")
        postos = response.json()
        posto_mais_proximo = None
        distancia_mais_proxima = float("inf")
        for posto in postos:
            distancia = self.calcular_distancia(self.latitude, self.longitude, posto["latitude"], posto["longitude"])
            if posto["energia"] > 0 and distancia < distancia_mais_proxima and posto["fila"] == min([p["fila"] for p in postos]):
                posto_mais_proximo = posto
                distancia_mais_proxima = distancia
        return posto_mais_proximo

    def calcular_distancia(self, lat1, long1, lat2, long2):
        # cálculo simplificado da distância entre dois pontos em uma esfera
        return ((lat1 - lat2) ** 2 + (long1 - long2) ** 2) ** 0.5

    def enviar_mensagem(self, mensagem):
        self.client_mqtt.publish(MQTT_TOPIC, mensagem.encode('utf-8'))

    def receber_mensagem(self, mensagem):
        mensagem_decodificada = mensagem.decode('utf-8')
        mensagem_json = json.loads(mensagem_decodificada)
        if mensagem_json["tipo"] == "abastecer":
            posto_id = mensagem_json["posto_id"]
            energia = mensagem_json["energia"]
            response = requests.put(f"{REST_API_URL}/postos/{posto_id}{REST_API_ROTA_ABASTECE_POSTO}", json={"energia": energia})
            if response.status_code == 200:
                print(f"Abastecimento realizado com sucesso no posto {posto_id}. Energia: {energia}")
            else:
                print(f"Falha ao abastecer no posto {posto_id}. Status code: {response.status_code}")
                
    def conectar_mqtt(self):
        self.client_mqtt.on_connect = lambda client, userdata, flags, rc: self.client_mqtt.subscribe(MQTT_TOPIC)
        self.client_mqtt.on_message = lambda client, userdata, msg: self.receber_mensagem(msg.payload)
        self.client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client_mqtt.loop_forever()