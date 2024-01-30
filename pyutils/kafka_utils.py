from __future__ import annotations

from typing import TypeAlias, Generator, Optional, Any
from collections.abc import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
import sys

from kafka import KafkaConsumer, KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import NoBrokersAvailable

from .types import KeyValue
from .utils import utc_now_millis


class KafkaEvent(ABC):
    __slots__ = ()
    
    @abstractmethod
    def key(self) -> str:
        """Returns key value for Kafka Producer record.

        Returns:
            str: key value for Kafka Producer record.
        """
        ...
    
    @abstractmethod
    def to_kafka_record(self) -> KeyValue[bytes, bytes]:
        """Returns encoded value for Kafka Producer record.

        Returns:
            KeyValue[bytes, bytes]: encoded key and value for Kafka Producer record.
        """
        ...
        
    @staticmethod
    @abstractmethod
    def from_kafka_record(record:ConsumerRecord) -> KafkaEvent:
        ...


def open_kafka_consumer(kafka_brokers:str, kafka_offset:str,
                        key_deserializer:Callable[[bytes],str]=lambda k:k.decode('utf-8'),
                        value_deserializer:Optional[Callable[[bytes],Any]]=None,
                        **options) -> KafkaConsumer:
    consumer = KafkaConsumer(bootstrap_servers=kafka_brokers, auto_offset_reset=kafka_offset,
                             key_deserializer=key_deserializer,
                             value_deserializer=value_deserializer)
    if 'topics' in options:
        consumer.subscribe(options['topics'])
    return consumer


def open_kafka_producer(brokers:list[str], *,
                        key_serializer:Callable[[str],bytes]=lambda k: k.encode('utf-8')) -> KafkaProducer:
    try:
        return KafkaProducer(bootstrap_servers=brokers, key_serializer=key_serializer)
    except NoBrokersAvailable as e:
        raise NoBrokersAvailable(f'fails to connect to Kafka: server={brokers}')


@dataclass(frozen=True, eq=True, order=True, unsafe_hash=True, slots=True)
class PollTimeout:
    elapsed_ms: int


KafkaPollData:TypeAlias = ConsumerRecord|PollTimeout 
KAFKA_POLL_ARG_NAMES = {'timeout_ms', 'max_records', 'update_offsets'}

def read_topics(consumer:KafkaConsumer, **options) -> Generator[KafkaPollData, bool, None]:
    # 'initial_timeout_ms'가 지정된 경우는 첫번째 poll() 메소드를 호출하는 경우의 timeout_ms은
    # 'timeout_ms'를 사용하지 않고, 이것을 사용하도록 일시적으로 변경시켜 사용한 후 다음부터는
    # 원래의 'timeout_ms'를 사용하도록 한다.
    timeout = options.get('timeout', sys.maxsize)
    poll_timeout = options.get('poll_timeout', 1000)
    initial_poll_timeout = options.get('initial_poll_timeout', poll_timeout)
    close_on_return = options.get('close_on_return', False)
    drop_poll_timeout = options.get('drop_poll_timeout', False)
    
    poll_args = { k:v for k, v in options.items() if k in KAFKA_POLL_ARG_NAMES }
    poll_args['timeout_ms'] = initial_poll_timeout
    timeout_elapsed = 0
    try:
        while True:
            started = utc_now_millis()
            partitions = consumer.poll(**poll_args)
            if partitions:
                timeout_elapsed = 0
                for _, partition in partitions.items():
                    for record in partition:
                        stop:bool = yield record
                        if stop: return
                poll_args['timeout_ms'] = poll_timeout 
            else:
                timeout_elapsed += (utc_now_millis()-started)
                if timeout_elapsed >= timeout:
                    return
                
                if not drop_poll_timeout:
                    stop:bool = yield PollTimeout(elapsed_ms=timeout_elapsed)
                    if stop: return
    finally:
        if close_on_return:
            consumer.close()