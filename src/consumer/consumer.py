import asyncio

from consumer.config import KafkaConsumer
from data import db_handler


async def main():
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "my_group",
        "auto.offset.reset": "earliest",
    }

    session = await db_handler.get_db()
    consumer = KafkaConsumer(config, session)
    try:
        consumer.consume("topic_name")
    finally:
        consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
