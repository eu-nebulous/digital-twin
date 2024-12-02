This directory contains the programs that connect to the running demo
app and prints digital twin-relevant events as jsonl (one line per
JSON object), and then generate a SQLite database from the collected logs.

To execute, make sure that the fire app is running; start it via the
docker-compose file in this repository.

We run the scripts via [uv](https://docs.astral.sh/uv/)

```sh
kubectl -n prod port-forward service/dt-broker 31084:1883
uv run log-monitor.py > logs.jsonl
# Start the workload here ...
uv run db-generator.py logs.jsonl
```

This generates a SQLite file `trace.db`.
