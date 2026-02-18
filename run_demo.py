"""
Launch quick local demo (assumes docker-compose services are up).
This script is optional — docker-compose is recommended for local runs.
"""
import requests
def demo():
    payload = {"user_id": "demo", "text": "Should I launch a fintech startup targeting SMBs? Provide TAM, revenue ideas and initial costs."}
    r = requests.post("http://localhost:8000/api/strategic/market", json=payload, timeout=30)
    print(r.json())

if __name__ == "__main__":
    demo()
