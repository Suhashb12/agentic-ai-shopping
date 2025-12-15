import json
from datetime import datetime

MEMORY_FILE = "memory/history.json"

def save_interaction(user_input, response):
    record = {
        "time": str(datetime.now()),
        "input": user_input,
        "response": response
    }

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
