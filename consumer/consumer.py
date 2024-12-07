import pika
import time

def callback(ch, method, properties, body):
    print(f"[x] Reçu : {body.decode()}")
    # Simuler un traitement (par exemple, une tâche longue)
    time.sleep(2)
    print("[x] Traitement terminé")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Boucle pour attendre RabbitMQ
while True:
    try:
        print("Tentative de connexion à RabbitMQ...")
        # Établir la connexion
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq')  # Le nom de service Docker de RabbitMQ
        )
        channel = connection.channel()

        # Déclarer la queue
        channel.queue_declare(queue='task_queue', durable=True)

        # Configurer la consommation de messages
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)

        print("[*] En attente de messages. Appuyez sur CTRL+C pour quitter.")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ n'est pas prêt. Nouvelle tentative dans 5 secondes...")
        time.sleep(5)  # Attendre avant une nouvelle tentative
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur. Fermeture...")
        break


