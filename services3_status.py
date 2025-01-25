import requests

PROMETHEUS_URL = "https://prometheus.aralvesandrade.duckdns.org/api/v1/query"
SERVICES = {
    "CORE": ["portainer", "prometheus", "grafana", "sonarqube"],
    "DATABASE": ["postgres", "mysql", "mongo", "redis"],
    "APPS": ["ecom-api", "ipool-api"],
}

STATUS_MESSAGES = {
    "0": "DOWN",
    "1": "MAINTENANCE",
    #"1": "UP",
    "2": "PENDING",
    "3": "MAINTENANCE"
}


def get_service_status(service):
    """Consulta o Prometheus e retorna o status de um serviço."""
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


def format_columns(services_dict):
    """Formata os serviços em colunas."""
    rows = []
    max_rows = max(len(services) for services in services_dict.values())

    # Preenche os serviços para alinhar as colunas
    for i in range(max_rows):
        row = []
        for category in services_dict.keys():
            if i < len(services_dict[category]):
                service = services_dict[category][i]
                status = get_service_status(service)
                row.append(f"{service}: {status}")
            else:
                row.append("")  # Espaço vazio para alinhar
        rows.append(row)

    # Cria a saída formatada
    output = ["CORE".ljust(24) + "| DATABASE".ljust(24) + "| APPS"]
    for row in rows:
        output.append(
            f"{row[0].ljust(24)}{'| ' + row[1].ljust(22)}{'| ' + row[2]}"
        )
    return "\n".join(output)


if __name__ == "__main__":
    services_by_category = {category: services for category, services in SERVICES.items()}
    print(format_columns(services_by_category))
