This directory contains the programs that connect to the running demo
app and prints digital twin-relevant events as jsonl (one line per
JSON object), and then generate a SQLite database from the collected logs.

To execute, make sure that the fire app is running; start it via the
docker-compose file in this repository.

We run the scripts via [uv](https://docs.astral.sh/uv/)

Logs are collected in a SQLite file `trace.db`.

# One-shot database generation

1. start FIRE demo app
2. start monitor
3. run FIRE demo workload
4. Convert / use database

```sh
kubectl -n prod port-forward service/dt-broker 31084:1883
uv run activemq-to-log.py > logs.jsonl
# Start the workload here to fill logs.jsonl
uv run log-to-db.py logs.jsonl
```

# Continuous collection (untested)

1. start FIRE demo app
2. start monitor
3. run FIRE demo workload

```sh
kubectl -n prod port-forward service/dt-broker 31084:1883
uv run activemq-to-db.py
# Start the workload here to fill trace.db
```
