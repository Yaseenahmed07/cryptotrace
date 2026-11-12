import hashlib
import json
from datetime import datetime


def create_audit_entry(action, details):
    entry = {
        "time": datetime.now().isoformat(),
        "action": action,
        "details": details
    }

    return entry


def calculate_hash(entry, previous_hash):
    data = json.dumps(entry, sort_keys=True)
    combined = data + previous_hash

    return hashlib.sha256(
        combined.encode()
    ).hexdigest()


def save_audit_log(action, details):
    filename = "audit_log.json"

    try:
        with open(filename, "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    previous_hash = (
        logs[-1]["hash"] if logs else "GENESIS"
    )

    entry = create_audit_entry(action, details)
    entry["previous_hash"] = previous_hash
    entry["hash"] = calculate_hash(entry, previous_hash)

    logs.append(entry)

    with open(filename, "w") as file:
        json.dump(logs, file, indent=4)

    return entry["hash"]
import hashlib
import json


def verify_audit_log(filename="audit_log.json"):
    try:
        with open(filename, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    previous_hash = "GENESIS"

    for entry in logs:

        # Check the previous hash link
        if entry.get("previous_hash") != previous_hash:
            return False

        # Reconstruct the original entry
        data = {
            "time": entry["time"],
            "action": entry["action"],
            "details": entry["details"],
            "previous_hash": previous_hash
        }

        serialized = json.dumps(data, sort_keys=True)
        combined = serialized + previous_hash

        calculated_hash = hashlib.sha256(
            combined.encode()
        ).hexdigest()

        if calculated_hash != entry["hash"]:
            return False

        previous_hash = entry["hash"]

    return True
