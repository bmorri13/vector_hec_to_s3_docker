import requests
import json
import time
from random import randint, choice

# List of sample actions and animals for more diverse event messages
actions = ["left the barn", "entered the barn", "won the race", "is taking a nap", "is looking for food"]
animals = ["Pony", "Chicken", "Cow", "Sheep", "Goat"]

def send_events_to_splunk(hec_url, token, events):
    headers = {
        'Authorization': f'Splunk {token}',
        'Content-Type': 'application/json'
    }
    # Format events as separate JSON objects on new lines
    data = '\n'.join(json.dumps(event) for event in events)
    response = requests.post(hec_url, headers=headers, data=data)
    return response

def generate_random_event(sourcetype=None):
    animal = choice(animals)
    action = choice(actions)
    event_number = randint(1, 1000)  # Random event identifier
    temperature = randint(-10, 40)  # Random temperature
    humidity = randint(20, 80)  # Random humidity percentage
    timestamp = int(time.time())  # Current time in UNIX epoch format
    event_data = {
        "time": timestamp,
        "sourcetype": sourcetype, 
        "event":{
            "animal": animal,
            "event_number": event_number,
            "action": action,
            "temperature": temperature,
            "humidity": humidity
        },
        "details": {
            "temperature": f"{temperature}°C",
            "humidity": f"{humidity}%",
            "action_details": f"Details about {action}."
        }
    }
    return event_data

def main():
    ## Variables
    sourcetype="vector_test"

    hec_url = "http://localhost:8088/services/collector"
    token = "A94A8FE5CCB19BA61C4C08"
    duration = 5 * 60  # Run for 5 minutes
    end_time = time.time() + duration
    
    while time.time() < end_time:
        events_batch = [generate_random_event(sourcetype=sourcetype) for _ in range(100)]
        response = send_events_to_splunk(hec_url, token, events_batch)
        print(f'Sent batch of events, Status Code: {response.status_code}')
        time.sleep(20)  # Wait for 20 seconds before sending the next batch

if __name__ == "__main__":
    main()
