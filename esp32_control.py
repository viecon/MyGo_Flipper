import requests

ESP_IP = "192.168.50.214"
ESP_PORT = 80
ESP_API_URL = f"http://{ESP_IP}:{ESP_PORT}/spin"


def control_esp(value):
    data = {"position": value}
    response = requests.post(ESP_API_URL, json=data)
    return response.json()
