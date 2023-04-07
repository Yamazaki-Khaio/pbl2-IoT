from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import requests

app = Flask(__name__)

# Configuração da conexão MQTT
mqtt_broker_address = "mqtt.example.com"
mqtt_broker_port = 1883
mqtt_client = mqtt.Client("car-computing")
try:
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
except ConnectionRefusedError as e:
    print(f"Erro ao se conectar ao broker MQTT: {e}")

# Configuração da conexão API REST
api_url = "http://api.example.com/gas-stations"
api_token = "my_api_token"