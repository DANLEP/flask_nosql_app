import psutil
import requests
import time

MEMORY_THRESHOLD = 70
CHECK_INTERVAL = 60


def send_alarm(memory_usage):
    url = "https://api.docusketch.com/api/v1/alarm"
    payload = {
        "memory_usage": memory_usage,
        "message": "Memory usage exceeded threshold"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Alarm sent successfully. Status code: {response.status_code}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")


if __name__ == '__main__':
    while True:
        current_memory_usage = psutil.virtual_memory().percent
        print(f"Current memory usage: {current_memory_usage}%")

        if current_memory_usage > MEMORY_THRESHOLD:
            print("Memory threshold exceeded, sending alarm...")
            send_alarm(current_memory_usage)

        time.sleep(CHECK_INTERVAL)
