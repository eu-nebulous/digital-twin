import argparse
import json
import sqlite3


required_keys = {"CompName", "ReplicaID", "EventType", "EventTime",
                 "PayloadSize", "ActivityID", "RemoteCompName"}


def process_file(tracefile, dbfile):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS trace_events')
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trace_events(
       local_name STRING,
       local_id STRING,
       remote_name STRING,
       activity_id STRING,
       event_type STRING,
       event_time INTEGER,
       payload_size INTEGER)""")
    cur.execute("DELETE FROM trace_events")
    for line_number, line in enumerate(tracefile, start=1):
        try:
            data = json.loads(line)
            if (required_keys.issubset(data.keys())):
                cur.execute("""
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
                print(f"Missing attributes in log line {line_number}: {required_keys - data.keys()}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in log line {line_number}")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS components(
      name STRING,
      replica_id STRING,
      cores INTEGER DEFAULT 0
    )
    """)
    cur.execute("DELETE FROM components")
    cur.execute("""
      INSERT INTO components (name, replica_id)
      SELECT DISTINCT local_name, local_id
        FROM trace_events
       UNION
      SELECT DISTINCT remote_name, ''
        FROM trace_events
       WHERE remote_name NOT IN (SELECT local_name FROM trace_events)""")
    con.commit()


def main():
    parser = argparse.ArgumentParser(
        description='Create SQLite database with trace information')
    parser.add_argument('tracefile', type=argparse.FileType('r'),
                        help='The trace file, in JSONL format')
    parser.add_argument('dbfile', type=str,
                        nargs='?', default='trace.db',
                        help='The database file to create (will be overwritten)')
    args = parser.parse_args()
    process_file(args.tracefile, args.dbfile)


if __name__ == "__main__":
    main()
