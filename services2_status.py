import requests

PROMETHEUS_URL = "https://prometheus.aralvesandrade.duckdns.org/api/v1/query"
SERVICES = {
    "core": ["portainer", "prometheus", "grafana", "sonarqube"],
    "database": ["postgres", "mysql", "mongo", "redis"],
    "apps": ["ecom-api", "ipool-api"],
}

STATUS_MESSAGES = {
    "0": "DOWN",
    "1": "UP",
    "2": "PENDING",
    "3": "MAINTENANCE"
}

def get_service_status(service):
    query = f'monitor_status{{monitor_name="{service}"}}'
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": query})
        response.raise_for_status()
        data = response.json()

        if data["status"] == "success":
            results = data["data"]["result"]
            if results:
                status_code = results[0]["value"][1]
                return STATUS_MESSAGES.get(status_code, "UNKNOWN")
            else:
                return "NOT FOUND"
        else:
            return "ERROR"
    except Exception:
        return "ERROR"

if __name__ == "__main__":
    output = []
    for category, services in SERVICES.items():
        output.append(f"{category.upper()}:")
        for service in services:
            status = get_service_status(service)
            output.append(f"{service}: {status}")
        output.append("")

    print("\n".join(output))
