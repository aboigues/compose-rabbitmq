# Utiliser une image Python de base
FROM python:3.9-slim

# Installer les dépendances
RUN pip install pika

# Copier le script dans le conteneur
COPY producer.py /app/producer.py
WORKDIR /app

# Commande par défaut
CMD ["python", "producer.py"]


