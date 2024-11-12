import asyncio
import json

from confluent_kafka import Consumer, KafkaError
from sqlalchemy.ext.asyncio import AsyncSession

from consumer.handlers import handle_data


class KafkaConsumer:
    def __init__(self, kafka_config: dict[str, str], session: AsyncSession):
        self.consumer = Consumer(kafka_config)
        self.session = session

    def consume(self, topic: str | list[str]):
        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    continue

            self.process_message(msg.value().decode("utf-8"))

    @staticmethod
    def process_message(message):
        data = json.loads(message)
        asyncio.create_task(handle_data(data))

    def close(self):
        self.consumer.close()
