# REPOSITORIO DESTINADO AO PROBLEMA 2 DA DISCIPLINA MI - Concorrência e Conectividade - 2023.1


# Organização das pastas
A solução está organizada duas pastas(pythonProject/models) e três arquivos executavéis, com o Diagrama de Sequência básico da arquitetura, executaveis python do servidor, medidor e usuarioe tambem contém dois arquivos dockerfiles para criação da imagem do Servidor e Medidor. Na pasta models está presente todos os modelos necessários para executar a solução, sendo dois executáveis via PYTHON, sendo eles: o cliente "medidor.py", usuario "usuario.py" e o servidor "servidor.py", .

# RELATÓRIO

Este relatório descreve o funcionamento de um sistema de gerenciamento de carga para carros elétricos que utiliza a arquitetura de computação em névoa (fog computing). O código foi desenvolvido em Python e utiliza a biblioteca Paho MQTT para a comunicação entre os diferentes nós do sistema.

O sistema é composto por três nós: o MQTT Broker, o fog node e o edge node. O MQTT Broker é responsável por receber as mensagens dos sensores instalados nos carros elétricos e nos postos de recarga e encaminhá-las para os nós adequados. O fog node é responsável por processar as mensagens dos carros elétricos e o edge node é responsável por processar as mensagens dos postos de recarga.

As mensagens dos carros elétricos contêm informações sobre a carga da bateria e o tipo de descarga (rápida ou lenta). O fog node processa essas informações e calcula o tempo de carregamento necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada para o edge node. As mensagens dos postos de recarga contêm informações sobre a capacidade do posto e a fila de espera. O edge node processa essas informações e calcula o tempo de espera necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada de volta para o MQTT Broker.

O sistema utiliza variáveis para controle da carga de processamento dos nós. O fog node possui uma capacidade máxima de processamento definida pela variável fog_capacity. O edge node possui uma capacidade máxima de processamento definida pela variável edge_capacity. As variáveis fog_load e edge_load contêm a carga atual de processamento dos nós e são atualizadas a cada mensagem processada.

O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. Essas mensagens são publicadas no MQTT Broker e encaminhadas para os nós adequados para processamento.

O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker. A função mqtt_loop é executada em uma thread separada e é responsável por manter a conexão com o MQTT Broker e receber as mensagens. A função on_message é executada em uma thread separada e é responsável por chamar as funções de processamento de dados de acordo com o tópico da mensagem recebida.

Em resumo, o sistema implementado é capaz de gerenciar a carga de carros elétricos em uma rede de postos de recarga utilizando a arquitetura de fog computing. O sistema utiliza a biblioteca Paho MQTT para a comunicação entre os diferentes nós e utiliza variáveis para controle da carga de processamento dos nós. O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. As mensagens são processadas pelos nós adequados e as informações de tempo de carregamento ou tempo de espera são adicionadas às mensagens antes de serem encaminhadas de volta para o MQTT Broker. O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker.

# FUNCIONAMENTO

Este código é um exemplo de simulação de comunicação entre dispositivos IoT (Internet das Coisas) utilizando o protocolo MQTT (Message Queuing Telemetry Transport).

Inicialmente, as configurações dos brokers, tópicos, nós fog e edge são definidas. As variáveis para controle da carga de processamento dos nós também são inicializadas. Em seguida, são definidas duas funções que processam dados: a primeira processa dados de carros elétricos e publica no tópico do fog node, enquanto a segunda processa dados de postos de recarga e publica no tópico do edge node.

Em seguida, é criado um cliente MQTT, que se conecta ao broker e se inscreve em dois tópicos: "dadoscarros" e "dadospontos". O loop de recebimento de mensagens é iniciado em uma thread separada para que a conexão com o broker seja mantida enquanto a aplicação continua a executar.

Após isso, um loop principal é iniciado para gerar e publicar dados aleatórios de carros elétricos e postos de recarga, respectivamente, utilizando funções específicas. Esses dados são gerados aleatoriamente e incluem informações como ID do carro, marca, modelo, porcentagem de bateria, tipo de descarga, ID do posto de recarga, capacidade do posto, tamanho da fila e localização.

Em resumo, o código simula o envio de dados entre dispositivos IoT através do protocolo MQTT, permitindo o processamento desses dados em diferentes nós (fog e edge) e o gerenciamento da carga de processamento em cada nó.
