import os
from kafka import KafkaConsumer, KafkaProducer
from dotenv import load_dotenv
load_dotenv(".env")

producer_config = {
    'bootstrap_servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl_mechanism': os.getenv('SASL_MECHANISM'),
    'security_protocol': os.getenv('SECURITY_PROTOCOL'),
    'sasl_plain_username': os.getenv('SASL_PLAIN_USERNAME'),
    'sasl_plain_password': os.getenv('SASL_PLAIN_PASSWORD'),
}


def get_kafka_consumer(topicname: str) -> KafkaConsumer:
    """
    Get Kafka Consumer from topic name.

    Args:
        topicname (str): Name of the kafka topic.
    Returns:
        KafkaConsumer
    """
    return KafkaConsumer(topicname,
                         bootstrap_servers=producer_config["bootstrap_servers"],
                         sasl_mechanism=producer_config["sasl_mechanism"],
                         security_protocol=producer_config["security_protocol"],
                         sasl_plain_username=producer_config["sasl_plain_username"],
                         sasl_plain_password=producer_config["sasl_plain_password"],
                         value_deserializer=lambda x: x.decode('utf-8'))


def get_kafka_producer() -> None:
    """
    Get Kafka Producer.
    """
    return KafkaProducer(bootstrap_servers=producer_config["bootstrap_servers"],
                         sasl_mechanism=producer_config["sasl_mechanism"],
                         security_protocol=producer_config["security_protocol"],
                         sasl_plain_username=producer_config["sasl_plain_username"],
                         sasl_plain_password=producer_config["sasl_plain_password"])
