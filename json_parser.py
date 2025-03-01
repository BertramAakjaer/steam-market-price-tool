import json

def get_config():
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        return [(data['name'], data['hash']) for key, data in config.items()]
    except FileNotFoundError:
        print("Error: config.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json.")
        return []