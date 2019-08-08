#!/usr/bin/env python36

import pika
import ssl

certs="../logbuffer-ops/rabbitmq/certs"

print("Certs path:", certs)

ssl_opts = {
    'ca_certs': 'certs/cacert.pem',
    'certfile': 'certs/cert.pem',
    'keyfile': 'certs/key.pem',
    'cert_reqs': ssl.CERT_REQUIRED,
    'ssl_version': ssl.PROTOCOL_TLSv1_2
}

rabbit_opts = {
    'host': '127.0.0.1',
    'port': 5671,
    'user': 'tony-ops',
    'password': 'tony-ops',
}

rabbit_queue_opts = {
    'queue': 'logging',
    'message': 'Hello SSL World :)'
}

parameters = pika.ConnectionParameters(host=rabbit_opts['host'],
                                       port=rabbit_opts['port'],
                                       credentials=pika.PlainCredentials(rabbit_opts['user'], rabbit_opts['password']),
                                       ssl=True,
                                       ssl_options=ssl_opts)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue_opts['queue'])

    channel.basic_publish(exchange='',
                          routing_key=rabbit_queue_opts['queue'],
                          body=rabbit_queue_opts['message'])

    print(" [x] Sent '" + rabbit_queue_opts['message'] + "!'")

    connection.close()
except BaseException as e:
    print(str(e), e.__class__.__name__)
