# REPOSITORIO DESTINADO AO PROBLEMA 2 DA DISCIPLINA MI - Concorrência e Conectividade - 2023.1


# Organização das pastas
A solução está organizada em 3 três arquivos executavéis, com o Diagrama de Sequência básico da arquitetura, executaveis python do servidor, medidor e usuarioe tambem contém dois arquivos dockerfiles para criação da imagem do Servidor e Medidor. Na pasta models está presente todos os modelos necessários para executar a solução, sendo dois executáveis via PYTHON, sendo eles: o cliente "medidor.py", usuario "usuario.py" e o servidor "servidor.py", .

# RELATÓRIO

Este relatório descreve o funcionamento de um sistema de gerenciamento de carga para carros elétricos que utiliza a arquitetura de computação em névoa (fog computing). O código foi desenvolvido em Python e utiliza a biblioteca Paho MQTT para a comunicação entre os diferentes nós do sistema.

O sistema é composto por três nós: o MQTT Broker, o fog node e o edge node. O MQTT Broker é responsável por receber as mensagens dos sensores instalados nos carros elétricos e nos postos de recarga e encaminhá-las para os nós adequados. O fog node é responsável por processar as mensagens dos carros elétricos e o edge node é responsável por processar as mensagens dos postos de recarga.

As mensagens dos carros elétricos contêm informações sobre a carga da bateria e o tipo de descarga (rápida ou lenta). O fog node processa essas informações e calcula o tempo de carregamento necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada para o edge node. As mensagens dos postos de recarga contêm informações sobre a capacidade do posto e a fila de espera. O edge node processa essas informações e calcula o tempo de espera necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada de volta para o MQTT Broker.

O sistema utiliza variáveis para controle da carga de processamento dos nós. O fog node possui uma capacidade máxima de processamento definida pela variável fog_capacity. O edge node possui uma capacidade máxima de processamento definida pela variável edge_capacity. As variáveis fog_load e edge_load contêm a carga atual de processamento dos nós e são atualizadas a cada mensagem processada.

O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. Essas mensagens são publicadas no MQTT Broker e encaminhadas para os nós adequados para processamento.

O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker. A função mqtt_loop é executada em uma thread separada e é responsável por manter a conexão com o MQTT Broker e receber as mensagens. A função on_message é executada em uma thread separada e é responsável por chamar as funções de processamento de dados de acordo com o tópico da mensagem recebida.

Em resumo, o sistema implementado é capaz de gerenciar a carga de carros elétricos em uma rede de postos de recarga utilizando a arquitetura de fog computing. O sistema utiliza a biblioteca Paho MQTT para a comunicação entre os diferentes nós e utiliza variáveis para controle da carga de processamento dos nós. O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. As mensagens são processadas pelos nós adequados e as informações de tempo de carregamento ou tempo de espera são adicionadas às mensagens antes de serem encaminhadas de volta para o MQTT Broker. O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker.

# FUNCIONAMENTO

O código implementa uma solução de IoT para gerenciamento de carregamento de veículos elétricos em uma infraestrutura de computação em névoa (fog computing) e borda (edge computing). O objetivo é balancear a carga de processamento entre os nós de computação para melhorar o desempenho e a eficiência do sistema.

O código utiliza a biblioteca Paho MQTT para implementar a comunicação entre os nós e os dispositivos IoT. Os dados dos dispositivos são enviados para um broker MQTT, que encaminha os dados para os nós de computação apropriados (fog ou edge) com base em suas capacidades de processamento.

O código define duas funções principais para processar os dados dos dispositivos: process_car_data() e process_posto_data(). A primeira função processa os dados de um carro elétrico e determina em qual nó de computação o carro deve ser processado com base em sua localização e na carga de processamento dos nós. A segunda função processa os dados de um posto de recarga e determina se o posto deve ser processado na borda ou na névoa com base na carga de processamento dos nós.

O código também define uma função monitor_load() que monitora a carga de processamento dos nós e ajusta a capacidade dos nós de acordo com a carga para manter um bom desempenho do sistema.

O padrão de desenvolvimento utilizado neste código é o de programação concorrente com threads. O código cria uma thread separada para monitorar a carga dos nós e ajustar a capacidade, enquanto outras threads são criadas para processar os dados dos dispositivos.

Em resumo, o código implementa uma solução de IoT para gerenciamento de carregamento de veículos elétricos em uma infraestrutura de fog e edge computing, utilizando a biblioteca Paho MQTT e programação concorrente com threads.
