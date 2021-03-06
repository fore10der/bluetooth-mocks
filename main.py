import threading

import bluetooth
import random
import json
import time


def get_random_data():
    return {
        "temperature": random.randint(-20, 20),
        "humidity": random.randint(0, 600),
        "light": random.random(),
    }


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

measures = get_random_data()
client_sock.send(str(measures))

try:
    while True:
        time.sleep(5)
        measures = get_random_data()
        client_sock.send(str(measures))
        print("Data sent", measures)
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
