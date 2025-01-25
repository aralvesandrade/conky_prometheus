import requests

PROMETHEUS_URL = "https://prometheus.aralvesandrade.duckdns.org/api/v1/query"
SERVICES = [
    "portainer", "prometheus", "grafana", "sonarqube",
    "postgres", "mysql", "mongo", "redis", "ecom-api", "ipool-api"
]

STATUS_MESSAGES = {
    "0": "DOWN",
    "1": "UP",
    "2": "PENDING",
    "3": "MAINTENANCE"
}

def monitor_service(service):
    query = f'monitor_status{{monitor_name="{service}"}}'

    try:
        response = requests.get(PROMETHEUS_URL, params={"query": query})
        response.raise_for_status()
        data = response.json()

        if data["status"] == "success":
            results = data["data"]["result"]
            if results:
                status_code = results[0]["value"][1]
                status_message = STATUS_MESSAGES.get(status_code, "UNKNOWN STATUS")
                print(f"{service.upper()}: {status_message}")
            else:
                print(f"{service.upper()}: Métrica não encontrada no Prometheus")
        else:
            print(f"Erro no retorno do Prometheus para {service.upper()}: {data.get('error', 'Erro desconhecido')}")

    except requests.exceptions.RequestException as req_err:
        print(f"Erro de conexão ao consultar {service.upper()}: {req_err}")
    except Exception as e:
        print(f"Erro inesperado ao processar {service.upper()}: {e}")

if __name__ == "__main__":
    # print("Monitorando status dos serviços:\n")
    for service in SERVICES:
        monitor_service(service)
