import time
import threading
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Define the MQTT broker settings
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic_postos = "dadosedge"
mqtt_topic_carros = "dadosfog"

# Define a variable to hold the charging station data
charging_stations = []
carro_station = []

# Configuração do cliente MQTT e inscrição nos tópicos
def on_message(client, userdata, message):
    if message.topic == mqtt_topic_postos:
        # Process the incoming message and add the charging station data to the list
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        charging_stations.append(data)

    elif message.topic == mqtt_topic_carros:
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        carro_station.append(data)

client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(mqtt_topic_postos, qos=0)
client.subscribe(mqtt_topic_carros, qos=0)

def mqtt_loop():
    while True:
        try:
            client.loop_forever()
        except Exception as e:
            print(f"Erro ao conectar ao broker: {e}")
            time.sleep(5)

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()



@app.route('/charging_stations', methods=['GET'])
def get_shortest_queue():
    # Sort the charging stations by queue length
    sorted_stations = sorted(charging_stations, key=lambda x: x["fila"])

    # Get the first station in the sorted list (i.e. the one with the shortest queue)
    shortest_queue_station = sorted_stations[0]

    # Return the station data as JSON
    return jsonify(shortest_queue_station)



@app.route('/carro', methods=['GET'])
def get_low_baterry():
    try:
        sorted_carro = sorted(carro_station, key=lambda x: x["bateria"])
        low_baterry = sorted_carro[0]
    except KeyError:
        return jsonify({"message": "Dados de bateria não encontrados."}), 404

    get_low_battery_and_shortest_queue()
    return jsonify(low_baterry)

def get_low_battery_and_shortest_queue():
    try:
        # Sort the charging stations by queue length and get the first station in the sorted list
        shortest_queue_station = sorted(charging_stations, key=lambda x: x["fila"])[0]

        # Sort the cars by battery level and get the car with the lowest battery level
        low_battery_car = sorted(carro_station, key=lambda x: x["bateria"])[0]

        # Print the message with the data
        print("Posto com menor fila:\nID: {}\nCapacidade: {}\nFila: {}\nLocalização: {}\nTempo de espera: {}".format(
            shortest_queue_station['id'],
            shortest_queue_station['capacidade'],
            shortest_queue_station['fila'],
            shortest_queue_station['localizacao'],
            shortest_queue_station['tempo_espera']
        ))
        print("\n")
        print("Carro com a menor bateria:\nID: {}\nMarca: {}\nModelo: {}\nBateria: {}\nDescarga: {}\nTempo de carga: {}".format(
            low_battery_car['id'],
            low_battery_car['marca'],
            low_battery_car['modelo'],
            low_battery_car['bateria'],
            low_battery_car['descarga'],
            low_battery_car['tempo_carregamento']
        ))

    except IndexError:
        print("Dados não encontrados.")


if __name__ == '__main__':
    app.run(debug=True)






