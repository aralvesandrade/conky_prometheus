import requests

PROMETHEUS_URL = "https://prometheus.aralvesandrade.duckdns.org/api/v1/query"
QUERY = 'monitor_status{monitor_name="mysql"}'

try:
    response = requests.get(PROMETHEUS_URL, params={"query": QUERY})
    data = response.json()

    if data["status"] == "success":
        results = data["data"]["result"]
        if results:
            status = results[0]["value"][1]
            status_message = "UP" if status == "1" else "DOWN"
            print(f"MySQL: {status_message}")
        else:
            print("MySQL: Métrica não encontrada")
    else:
        print("Erro na consulta ao Prometheus")
except Exception as e:
    print(f"Erro: {e}")
