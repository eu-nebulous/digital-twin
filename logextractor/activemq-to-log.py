import sys
import paho.mqtt.client as mqtt
import argparse
import json

required_keys = {"CompName", "ReplicaID", "EventType", "EventTime",
                 "PayloadSize", "ActivityID", "RemoteCompName"}


def on_message(client, userdata, message):
    line = message.payload.decode('utf-8')
    try:
        data = json.loads(line)
        if (required_keys.issubset(data.keys())):
            # This prints the message in one line (i.e., produces jsonl)
            print(line)
        else:
            print(f"Missing attributes in message {line}: {required_keys - data.keys()}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in message {line}")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason_code {reason_code}", file=sys.stderr)
    client.subscribe("nbls/dt/firecoat/update")


def main():
    parser = argparse.ArgumentParser(
        description='Listen to MQTT and print trace events to stdout')
    parser.add_argument('-p', '--mqttport', type=int, default=31084,
                        help='The port where to contact the MQTT broker (usually 1883 or 31084)')
    args = parser.parse_args()

    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Set the callbacks
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set(username="monitor", password="vxi*RseA8gmCNdt_6pYY")

    # Connect to the MQTT broker
    client.connect("localhost", args.mqttport, 60)

    # Start the network loop and process messages
    client.loop_forever()


if __name__ == "__main__":
    main()
