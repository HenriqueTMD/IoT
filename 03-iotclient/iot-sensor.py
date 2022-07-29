import random
import time

from paho.mqtt import client as mqtt_client

limite = 20
broker = '127.0.0.1'
port = 1883
topic1 = "iothon/bme280/sensor1"
topic2 = "iothon/bme280/sensor2"
topic3 = "iothon/bme280/semaforo1"
topic4 = "iothon/bme280/semaforo2"
topic5 = "iothon/bme280/contagem"
topic6 = "iothon/bme280/faixa"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqttuser'
password = 'mqttpassword'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # Inicialização
    msg_count = 0
    semaforo1 = 0
    semaforo2 = 2
    contagem = 0
    faixa = 0
    countTempo = 0

    # Inicia a faixa
    result = client.publish(topic6, faixa)
    status = result[0]
    if status == 0:
        print(f"Send `{faixa}` to topic `{topic6}`")
    else:
        print(f"Failed to send message to topic {topic6}")
    msg_count += 1

    # Inicia a semaforos
    result = client.publish(topic3, semaforo1)
    status = result[0]
    if status == 0:
        print(f"Send `{semaforo1}` to topic `{topic3}`")
    else:
        print(f"Failed to send message to topic {topic3}")
    msg_count += 1
    result = client.publish(topic4, semaforo2)
    status = result[0]
    if status == 0:
        print(f"Send `{semaforo2}` to topic `{topic4}`")
    else:
        print(f"Failed to send message to topic {topic4}")
    msg_count += 1

    # Inicia loop
    while True:
        # Verifica se a faixa da vez é a do sensor1 e se está com passagem aberta
        if semaforo1 != 2 and semaforo2 == 2 and faixa == 0:
            # Espera 5s
            time.sleep(5)

            # Gera um valor random para o sensor1 e envia a mensagem - (0,1 - passou um veiculo, nada aconteceu)
            msg = random. randint(0, 1)
            result = client.publish(topic1, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic1}`")
            else:
                print(f"Failed to send message to topic {topic1}")

            # Verifica se passou carro
            if msg == 1:
                # Aumenta o número de carros na via
                contagem += 1
                result = client.publish(topic5, contagem)
                status = result[0]
                if status == 0:
                    print(f"Send `{contagem}` to topic `{topic5}`")
                else:
                    print(f"Failed to send message to topic {topic5}")
                msg_count += 1

            # Aumenta a contagem de mensagens e a contagem usada para calcular o tempo
            msg_count += 1
            countTempo += 1

            # Verificação de passagem na faixa do sensor2
            # Espera 5s
            time.sleep(5)

            # Verificação se tem veiculo no trecho
            if contagem > 0:
                # Gera um valor random para o sensor2 e envia a mensagem - (0,1 - passou um veiculo, nada aconteceu)
                msg = random. randint(0, 1)
                result = client.publish(topic2, msg)
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{topic2}`")
                else:
                    print(f"Failed to send message to topic {topic2}")

                # Verifica se passou carro
                if msg == 1:
                    # Diminui o número de carros na via
                    contagem -= 1
                    result = client.publish(topic5, contagem)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{contagem}` to topic `{topic5}`")
                    else:
                        print(f"Failed to send message to topic {topic5}")
                    msg_count += 1

                # Aumenta a contagem de mensagens e a contagem usada para calcular o tempo
                msg_count += 1
            countTempo += 1

            # Verifica se a contagem de carros chegou a limite-2 ou tempo igual a 3m20s(40 msg)
            if contagem == (limite - 2) or countTempo == 40:
                # Altera semaforo para sinal Amarelo (1)
                semaforo1 = 1
                result = client.publish(topic3, semaforo1)
                status = result[0]
                if status == 0:
                    print(f"Send `{semaforo1}` to topic `{topic3}`")
                else:
                    print(f"Failed to send message to topic {topic3}")

            # Verifica se a contagem de carros chegou ao limite ou tempo igual a 3m40s(44 msg)
            if contagem == limite or countTempo == 44:
                # Altera semaforo para sinal Vermelho (2)
                semaforo1 = 2
                result = client.publish(topic3, semaforo1)
                status = result[0]
                if status == 0:
                    print(f"Send `{semaforo1}` to topic `{topic3}`")
                else:
                    print(f"Failed to send message to topic {topic3}")

        # Verifica se a faixa da vez é a do sensor2 e se está com passagem aberta
        elif semaforo1 == 2 and semaforo2 != 2 and faixa == 1:
            # Espera 5s
            time.sleep(5)

            # Gera um valor random para o sensor1 e envia a mensagem - (0,1 - passou um veiculo, nada aconteceu)
            msg = random. randint(0, 1)
            result = client.publish(topic2, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic2}`")
            else:
                print(f"Failed to send message to topic {topic2}")

            # Verifica se passou carro
            if msg == 1:
                # Aumenta o número de carros na via
                contagem += 1
                result = client.publish(topic5, contagem)
                status = result[0]
                if status == 0:
                    print(f"Send `{contagem}` to topic `{topic5}`")
                else:
                    print(f"Failed to send message to topic {topic5}")
                msg_count += 1

            # Aumenta a contagem de mensagens e a contagem usada para calcular o tempo
            msg_count += 1
            countTempo += 1

            # Verificação de passagem na faixa do sensor2
            # Espera 5s
            time.sleep(5)

            # Verificação se tem veiculo no trecho
            if contagem > 0:
                # Gera um valor random para o sensor1 e envia a mensagem - (0,1 - passou um veiculo, nada aconteceu)
                msg = random. randint(0, 1)
                result = client.publish(topic1, msg)
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{topic1}`")
                else:
                    print(f"Failed to send message to topic {topic1}")

                # Verifica se passou carro
                if msg == 1:
                    # Diminui o número de carros na via
                    contagem -= 1
                    result = client.publish(topic5, contagem)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{contagem}` to topic `{topic5}`")
                    else:
                        print(f"Failed to send message to topic {topic5}")
                    msg_count += 1

                # Aumenta a contagem de mensagens e a contagem usada para calcular o tempo
                msg_count += 1
            countTempo += 1

            # Verifica se a contagem de carros chegou a limite-2 ou tempo igual a 3m20s(40 msg)
            if contagem == (limite - 2) or countTempo == 40:
                # Altera semaforo para sinal Amarelo (1)
                semaforo2 = 1
                result = client.publish(topic4, semaforo2)
                status = result[0]
                if status == 0:
                    print(f"Send `{semaforo2}` to topic `{topic4}`")
                else:
                    print(f"Failed to send message to topic {topic4}")
                msg_count += 1

            # Verifica se a contagem de carros chegou ao limite ou tempo igual a 3m40s(44 msg)
            if contagem == limite or countTempo == 44:
                # Altera semaforo para sinal Vermelho (2)
                semaforo2 = 2
                result = client.publish(topic4, semaforo2)
                status = result[0]
                if status == 0:
                    print(f"Send `{semaforo2}` to topic `{topic4}`")
                else:
                    print(f"Failed to send message to topic {topic4}")
                msg_count += 1

        # Verifica se os semaforos estão ambos vermelhos
        elif semaforo1 == 2 and semaforo2 == 2:
            # Espera os carros sairem do trecho
            # Espera 5s
            time.sleep(5)
            # Verifica se o trecho está vazio
            if contagem == 0:
                # Reseta o tempo
                countTempo = 0
                # Verifica qual é a faixa da vez, altera e libera o semaforo correspondente
                if faixa == 0:
                    faixa = 1
                    semaforo2 = 0
                    result = client.publish(topic4, semaforo2)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{semaforo2}` to topic `{topic4}`")
                    else:
                        print(f"Failed to send message to topic {topic4}")
                    msg_count += 1
                    result = client.publish(topic6, faixa)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{faixa}` to topic `{topic6}`")
                    else:
                        print(f"Failed to send message to topic {topic6}")
                    msg_count += 1
                else:
                    faixa = 0
                    semaforo1 = 0
                    result = client.publish(topic3, semaforo1)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{semaforo1}` to topic `{topic3}`")
                    else:
                        print(f"Failed to send message to topic {topic3}")
                    msg_count += 1
                    result = client.publish(topic6, faixa)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{faixa}` to topic `{topic6}`")
                    else:
                        print(f"Failed to send message to topic {topic6}")
                    msg_count += 1
            else:
                msg = 0
                contagem -= 1
                if faixa == 0:
                    result = client.publish(topic2, msg)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{msg}` to topic `{topic2}`")
                    else:
                        print(f"Failed to send message to topic {topic2}")
                    msg_count += 1
                else:
                    result = client.publish(topic1, msg)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{msg}` to topic `{topic1}`")
                    else:
                        print(f"Failed to send message to topic {topic1}")
                    msg_count += 1
                result = client.publish(topic5, contagem)
                status = result[0]
                if status == 0:
                    print(f"Send `{contagem}` to topic `{topic5}`")
                else:
                    print(f"Failed to send message to topic {topic5}")
                msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
