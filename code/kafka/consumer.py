from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': 'd7tmih2e1n5c11g1k480.any.eu-west-2.mpx.prd.cloud.redpanda.com:9092',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'kafka-user',
    'sasl.password': 'Advaith@2010',
    'group.id': 'order-processor-2',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['orders'])

print("Listening for order events... (Ctrl+C to stop)")
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        order = json.loads(msg.value().decode('utf-8'))
        print(f"Received order: ID={order['order_id']} | "
              f"Customer={order['customer_id']} | "
              f"Product={order['product']} | "
              f"Amount=€{order['amount']} | "
              f"Offset={msg.offset()}")

except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
