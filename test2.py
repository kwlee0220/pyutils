from __future__ import annotations

from typing import Optional

import cv2
from kafka import KafkaConsumer, KafkaProducer

from pyutils.kafka_utils import read_topics, PollTimeout


consumer = KafkaConsumer(bootstrap_servers="localhost:9092", auto_offset_reset='earliest')
consumer.subscribe('global-tracks')
records = read_topics(consumer)
for data in records:
    if isinstance(data, PollTimeout) and data.elapsed_ms > 5000:
        records.send(True)
    print(data)