import pika
import time
import random

def send_message(channel, message):
    """
    Envoie un message à RabbitMQ via le canal donné.
    """
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Rendre le message persistant
        )
    )
    print(f"[x] Message envoyé : {message}")

def connect_to_rabbitmq():
    """
    Établit une connexion à RabbitMQ et retourne un canal valide.
    Si RabbitMQ n'est pas prêt, le script attend et réessaye.
    """
    while True:
        try:
            print("Tentative de connexion à RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq')  # Nom du service Docker RabbitMQ
            )
            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)
            print("[x] Connecté à RabbitMQ.")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ n'est pas disponible. Nouvelle tentative dans 5 secondes...")
            time.sleep(5)

def run_producer():
    """
    Lance le producteur pour envoyer des messages en boucle infinie.
    En cas de problème, il se reconnecte à RabbitMQ automatiquement.
    """
    while True:
        connection, channel = connect_to_rabbitmq()
        try:
            while True:
                # Génère un message aléatoire
                message = f"Message automatique {random.randint(1, 1000)}"
                #print("envoi message: "+ message)
                send_message(channel, message)
                time.sleep(1)  # Pause entre chaque envoi
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erreur de connexion : {e}. Réinitialisation...")
            time.sleep(5)  # Attendre avant une nouvelle tentative de connexion
        except Exception as e:
            print(f"Erreur inattendue : {e}. Réinitialisation...")
            time.sleep(5)
        finally:
            try:
                connection.close()
                print("[x] Connexion fermée proprement.")
            except Exception as e:
                print(f"Impossible de fermer la connexion : {e}")

if __name__ == "__main__":
    run_producer()


