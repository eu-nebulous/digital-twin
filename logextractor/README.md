This directory contains a small python program that connects to the
running demo app and prints digital twin-relevant events as jsonl (one
line per JSON object).

To execute, make sure that the fire app is running.

Run the script via [uv](https://docs.astral.sh/uv/):

    kubectl -n prod port-forward service/dt-broker 31084:1883
    uv run log-monitor.py

