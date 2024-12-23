import sys
import paho.mqtt.client as mqtt
import argparse
import json
import sqlite3


required_keys = {"CompName", "ReplicaID", "EventType", "EventTime",
                 "PayloadSize", "ActivityID", "RemoteCompName"}


def on_message(client, userdata, message):
    # This prints the message in one line (i.e., produces jsonl)
    cursor = userdata
    line = message.payload.decode('utf-8')
    try:
        data = json.loads(line)
        if (required_keys.issubset(data.keys())):
            cursor.execute("""
            INSERT INTO trace_events(
               local_name,
               local_id,
               remote_name,
               activity_id,
               event_type,
               event_time,
               payload_size)
            VALUES(
               :CompName,
               :ReplicaID,
               :RemoteCompName,
               :ActivityID,
               :EventType,
               :EventTime,
               :PayloadSize)""",
                           data)
        else:
            print(f"Missing attributes in message: {required_keys - data.keys()}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in message {message}")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason_code {reason_code}", file=sys.stderr)
    client.subscribe("nbls/dt/firecoat/update")


def main():
    parser = argparse.ArgumentParser(
        description='Listen on MQTT and create SQLite database with trace information')
    parser.add_argument('dbfile', type=str,
                        nargs='?', default='trace.db',
                        help='The database file, will be created if necessary')
    args = parser.parse_args()

    con = sqlite3.connect(args.dbfile)
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trace_events(
       local_name STRING,
       local_id STRING,
       remote_name STRING,
       activity_id STRING,
       event_type STRING,
       event_time INTEGER,
       payload_size INTEGER)""")
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS components(name, replica_id, cores) AS
    SELECT DISTINCT local_name, local_id, 0
      FROM trace_events
     UNION
    SELECT DISTINCT remote_name, '', 0
      FROM trace_events
     WHERE remote_name NOT IN (SELECT local_name FROM trace_events)
    """)

    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=cursor)
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
