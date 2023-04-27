import threading

from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Configurações do MQTT broker
broker_address = "172.16.103.13"
broker_port = 1883
broker_topic = "dadoscarros"
broker_topic_posto = "dadospontos"

# Armazena os dados dos carros
carros = {}

# Armazena os dados dos postos
postos = {}
# Callback que é chamado quando um novo payload é recebido no tópico MQTT correspondente
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    dados = json.loads(payload)
    tipo = dados.get("tipo")

    if topic == "fog" or topic == "edge":
        if tipo == "carro":
            carros[dados["id"]] = dados
        elif tipo == "posto":
            postos[dados["id"]] = dados
    elif topic == broker_topic_posto:
        id_posto = dados["id_posto"]
        if id_posto in postos:
            postos[id_posto]["fila"] = dados["fila"]


# Callback que é chamado quando um novo payload é recebido no tópico MQTT correspondente

# Configura o cliente MQTT e se inscreve nos tópicos correspondentes
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.subscribe(broker_topic, qos=1)
client.subscribe(broker_topic_posto, qos=1)
client.subscribe("fog", qos=1)
client.subscribe("edge", qos=1)

client.loop_start()


# Rota para visualizar um carro pelo id
# Rota para visualizar um carro pelo id
@app.route("/carros/<int:id>")
def visualizar_carro(id):
    with app.app_context():
        if id in carros:
            carro = carros[id]

            # Verifica se o carro está com a bateria baixa e busca o posto com a menor fila
            if carro["bateria"] < 100:
                posto_menor_fila = None
                for id_posto, posto in postos.items():
                    if posto_menor_fila is None or posto["fila"] < posto_menor_fila["fila"]:
                        posto_menor_fila = posto
                if posto_menor_fila is not None:
                    carro["posto_menor_fila"] = posto_menor_fila

            return jsonify(carro), 200, {'Content-Type': 'application/json; charset=utf-8', 'indent': 4}
        else:
            print(f"Carro não encontrado: {id}")
            return None


# Rota para visualizar o posto com a menor fila
@app.route("/postos/menorfila")
def visualizar_posto_menor_fila():
    posto_menor_fila = None
    for id, posto in postos.items():
        if posto_menor_fila is None or posto["fila"] < posto_menor_fila["fila"]:
            posto_menor_fila = posto
    if posto_menor_fila is not None:
        return jsonify(posto_menor_fila), 200, {'Content-Type': 'application/json; charset=utf-8', 'indent': 4}
    else:
        return jsonify({"erro": "Nenhum posto encontrado"}), 404, {'Content-Type': 'application/json; charset=utf-8', 'indent': 4}




# Função para exibir as informações de um carro e alertar sobre posto com menor fila
def exibir_carro_e_alerta(id):
    with app.app_context():
        carro = carros
        if carro is None:
            print(f"Carro não encontrado: {id}")
            return
        print("Informações do carro:")
        print(f"ID: {carro[id]['id']}")
        print(f"Modelo: {carro[id]['modelo']}")
        print(f"Bateria: {carro[id]['bateria']}")
        if carro[id]['bateria'] < 100:
            posto_menor_fila = carro.get("posto_menor_fila")
            if posto_menor_fila is not None:
                print(f"ALERTA: O posto {posto_menor_fila['nome']} tem a menor fila (posição {posto_menor_fila['fila']})")

def menu_principal():
    while True:
        print("Digite o ID do carro para visualizar suas informações (ou 'q' para sair):")
        input_id = input()
        if input_id == "q":
            break
        try:
            id = int(input_id)
            exibir_carro_e_alerta(id)
        except ValueError:
            print("ID inválido, por favor digite um número inteiro.")


if __name__ == "__main__":
    thread_menu = threading.Thread(target=menu_principal)
    thread_menu.start()
    app.run()
