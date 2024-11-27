import sys
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    # This prints the message in one line (i.e., produces jsonl)
    print(message.payload.decode('utf-8'))


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason_code {reason_code}", file=sys.stderr)
    client.subscribe("nbls/dt/firecoat/update")


def main():
    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Set the callbacks
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set(username="monitor", password="vxi*RseA8gmCNdt_6pYY")

    # Connect to the MQTT broker
    client.connect("localhost", 31084, 60)

    # Start the network loop and process messages
    client.loop_forever()


if __name__ == "__main__":
    main()
