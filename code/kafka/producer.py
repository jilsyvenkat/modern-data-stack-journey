from confluent_kafka import Producer
import json
import time
from datetime import datetime

conf = {
    'bootstrap.servers': 'd7tmih2e1n5c11g1k480.any.eu-west-2.mpx.prd.cloud.redpanda.com:9092',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'kafka-user',
    'sasl.password': 'Advaith@2010'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} partition [{msg.partition()}] offset {msg.offset()}')

orders = [
    {'order_id': 1, 'customer_id': 101, 'product': 'Laptop',  'amount': 999.99, 'status': 'placed'},
    {'order_id': 2, 'customer_id': 102, 'product': 'Phone',   'amount': 599.99, 'status': 'placed'},
    {'order_id': 3, 'customer_id': 103, 'product': 'Tablet',  'amount': 399.99, 'status': 'placed'},
    {'order_id': 4, 'customer_id': 101, 'product': 'Mouse',   'amount':  29.99, 'status': 'placed'},
    {'order_id': 5, 'customer_id': 104, 'product': 'Keyboard','amount':  79.99, 'status': 'placed'},
]

print("Producing order events...")
for order in orders:
    order['timestamp'] = datetime.now().isoformat()
    producer.produce(
        topic='orders',
        key=str(order['order_id']),
        value=json.dumps(order),
        callback=delivery_report
    )
    producer.poll(0)
    time.sleep(0.5)

producer.flush()
print("All orders produced successfully!")
