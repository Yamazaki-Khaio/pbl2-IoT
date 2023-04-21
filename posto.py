import paho.mqtt.client as mqtt
import json
from flask import Flask, jsonify
from typing import Callable
from collections import deque


app = Flask(__name__)

class PostoRecarga:
    MAX_CAPACIDADE = 10  # limite máximo de capacidade para os postos de recarga
    BROKER_HOST = "localhost"
    BROKER_PORT = 1883
    BROKER_TIMEOUT = 60

    def __init__(self, id: int, latitude: float, longitude: float, capacidade: int):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.capacidade = min(capacidade, PostoRecarga.MAX_CAPACIDADE)  # adiciona o limite máximo de capacidade
        self.fila = []

        self.client = None
        self.conectar()

    def __del__(self):
        self.desconectar()

    def conectar(self):
        # Cria um cliente MQTT e configura as funções de callback
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(PostoRecarga.BROKER_HOST, PostoRecarga.BROKER_PORT, PostoRecarga.BROKER_TIMEOUT)
            self.client.loop_start()
        except:
            print(f"Não foi possível conectar ao broker MQTT em {PostoRecarga.BROKER_HOST}:{PostoRecarga.BROKER_PORT}.")

    def desconectar(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def on_connect(self, client: mqtt.Client, userdata: None, flags: dict, rc: int):
        print("Conectado com sucesso no broker MQTT.")
        client.subscribe(f"posto-recarga/{self.id}/atualizar-fila")

    def on_message(self, client: mqtt.Client, userdata: None, msg: mqtt.MQTTMessage):
        topic = msg.topic.split("/")
        if len(topic) == 4 and topic[3] == "atualizar-fila":
            self.enviar_fila()

    def enviar_fila(self):
        num_carros = len(self.fila)
        payload = {"num_carros": num_carros}
        self.client.publish(f"posto-recarga/{self.id}/fila", json.dumps(payload).encode('utf-8'), qos=1)

    def adicionar_carro(self):
        if len(self.fila) < self.capacidade:
            self.fila.append(1)
            print(f"Carro adicionado à fila do posto de recarga {self.id}.")
        else:
            print(f"A fila do posto de recarga {self.id} já está cheia.")

    def remover_carro(self):
        if len(self.fila) > 0:
            self.fila.pop(0)
            print(f"Carro removido da fila do posto de recarga {self.id}.")
       


    def register_on_add_car_callback(self, callback: Callable):
        self.on_add_car_callback = callback

    def register_on_remove_car_callback(self, callback: Callable):
        self.on_remove_car_callback = callback

    def add_car(self):
        self.adicionar_carro()
        if hasattr(self, "on_add_car_callback"):
            self.on_add_car_callback(self)

    def remove_car(self):
        self.remover_carro()
        if hasattr(self, "on_remove_car_callback"):
            self.on_remove_car_callback(self)
postos = []

# Adiciona dois postos de recarga à lista de postos
posto1 = PostoRecarga(1, -23.5489, -46.6388, 2)
postos.append(posto1)

posto2 = PostoRecarga(2, -23.5505, -46.6361, 3)
postos.append(posto2)

@app.route("/postos")
def listar_postos():
    # Retorna a lista de postos de recarga disponíveis
    postos_json = []
    for posto in postos:
        postos_json.append({"id": posto.id, "latitude": posto.latitude, "longitude": posto.longitude, "capacidade": posto.capacidade})
    return jsonify(postos_json)



fila = deque()

@app.route('/adicionar_carro/<string:placa>', methods=['POST'])
def adicionar_carro(placa):
    if len(fila) < 10:
        fila.append(placa)
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="A fila está cheia")

@app.route('/remover_carro', methods=['DELETE'])
def remover_carro():
    if len(fila) > 0:
        fila.popleft()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="A fila está vazia")

if __name__ == '__main__':
    app.run()
# Adiciona um callback que é chamado sempre que um carro é adicionado a um posto
def on_add_car_callback(posto):
    print(f"Um carro foi adicionado à fila do posto de recarga {posto.id}.")
    posto.enviar_fila()

# Adiciona um callback que é chamado sempre que um carro é removido de um posto
def on_remove_car_callback(posto):
    print(f"Um carro foi removido da fila do posto de recarga {posto.id}.")
    posto.enviar_fila()

# Registra os callbacks para cada posto
posto1.register_on_add_car_callback(on_add_car_callback)
posto1.register_on_remove_car_callback(on_remove_car_callback)

posto2.register_on_add_car_callback(on_add_car_callback)
posto2.register_on_remove_car_callback(on_remove_car_callback)

# Adiciona alguns carros às filas dos postos
posto1.adicionar_carro()
posto2.adicionar_carro()
posto2.adicionar_carro()

# Remove um carro da fila do segundo posto
posto2.remover_carro()