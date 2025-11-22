# Sports Store Order Service

This repository contains a simple **order service** for a sports store.  It is built with **Python** and **Flask** and exposes business and system metrics via the Prometheus client library.  The project is containerised with Docker, packaged with **Helm** for deployment on Kubernetes, managed with **Terraform** and includes a basic GitHub Actions workflow for continuous integration and delivery.

## Features

- **RESTful API** – create and retrieve orders for sporting goods and view a catalogue of products.
- **Prometheus metrics** – business metrics (orders created, total amount, orders by category), request counters and histograms, and artificial error and latency simulations.
- **Health checks** – readiness and liveness endpoints to integrate with Kubernetes probes.
- **Containerised** – Docker image (arm64) that runs on your Mac.
- **Helm chart** – templated Kubernetes manifests for the application with optional ServiceMonitor for Prometheus scraping.
- **Infrastructure as Code** – sample Terraform configuration demonstrating how to install the Helm chart and manage it declaratively.
- **CI/CD pipeline** – GitHub Actions workflow to run tests, build and push the Docker image and publish it to GitHub Container Registry.

## Project structure

The repository is organised as follows:

```
.
├── app/                        # Application source code
│   ├── __init__.py
│   ├── app.py                  # Flask application factory and route definitions
│   ├── config.py               # Configuration class (environment variables)
│   ├── metrics.py              # Prometheus metric definitions
│   ├── models.py               # In‑memory data models for products and orders
│   └── utils.py                # Helper functions for failures and latency simulation
├── charts/                     # Helm charts
│   └── sports-store-app/       # Chart packaging this service
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── servicemonitor.yaml
├── terraform/                  # Example Terraform configuration
│   ├── main.tf
│   └── values/
│       └── sports-store-app-values.yaml
├── tests/                      # Basic tests for the service
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions pipeline
├── Dockerfile                  # Build definition for the application image
├── requirements.txt            # Python package dependencies
├── CONTRIBUTING.md             # Contribution guidelines
└── LICENSE                     # Project licence (MIT)
```

## Prerequisites

To run this project locally you will need:

* **Python 3.11** – for development and unit testing.
* **Docker** – container engine.  On macOS with M1 chips I used **Colima** as an alternative to Docker Desktop.
* **Minikube** – local Kubernetes cluster.  Use the `docker` driver and ensure Colima is running before starting Minikube.
* **Helm 3** – package manager for Kubernetes.
* **Terraform 1.5+** – optional: manage the Helm release declaratively.
* An SMTP account (e.g. Outlook) – for Alertmanager notifications (Still debugging an apparent SMTP error but run out of time).


## Quick start

### 1. Clone the repository

```sh
git clone https://github.com/your‑user/sports-store-order-service.git
cd sports-store-order-service
```

### 2. Run the service locally

1. Create a Python virtual environment and install dependencies:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Start the service:

    ```sh
    export ENVIRONMENT=local
    export FAILURE_RATE=0.0
    export SIMULATED_LATENCY_SECONDS=0.0
    python -m app.app
    ```

3. Access the API endpoints at `http://localhost:8000/`.

4. View Prometheus metrics at `http://localhost:8000/metrics`.

### 3. Build and run with Docker

Ensure Colima is running (`colima start`) then build and run the container:

```sh
# Build the multi‑arch image (amd64 and arm64)
docker buildx build --platform linux/arm64 -t little-ragnar/sports-store-order-service:latest --load .


# Run locally exposing port 8000
docker run --rm -p 8000:8000 little_ragnar/sports-store-order-service:latest
```

### 4. Deploy to Minikube with Helm

1. Ensure Colima and Minikube are running.  Start Minikube using the docker driver and allocate sufficient resources for Prometheus and Grafana:

    ```sh
    colima start
    minikube start --driver=docker --cpus=4 --memory=6000mb
    ````

2. Add the Prometheus Community Helm repository and update chart indices:

    ```sh
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    ```

3. Install the **kube-prometheus-stack** chart to deploy Prometheus, Grafana and Alertmanager:

    ```sh
    helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace --set prometheus.prometheusSpec.retention="2d" --set grafana.enabled=true --set alertmanager.enabled=true
    ```

4. Package and install this service’s Helm chart:

    ```sh
    # from the project root
    helm dependency update charts/sports-store-app && helm install sports-store-app charts/sports-store-app -n sports-store --create-namespace --set image.repository=little-ragnar/sports-store-order-service --set image.tag=latest
    ```

5. Verify the deployment:

    ```sh
    kubectl get pods -n sports-store
    kubectl get svc -n sports-store
    ```

The application should now be available within your Minikube cluster.  If you installed the kube-prometheus-stack and ServiceMonitor CRDs, Prometheus will automatically scrape the metrics exposed at `/metrics`.

### 5. Managing with Terraform

The `terraform/` directory contains a sample configuration that manages the Helm release of this application.  Edit `terraform/values/sports-store-app-values.yaml` to override chart values.  Initialise and apply the configuration:

```sh
cd terraform
terraform init
terraform apply
```

## Configuring Alertmanager and Outlook notifications (Esta al 90%, me encontre un smtp error que no he podido arreglar, pero pasos sencillos son estos)

If you installed the kube-prometheus-stack, Alertmanager is included.  To configure e‑mail notifications via Outlook (I created a test email):

Credentials:
Email - 'sre-ibm-test@outlook.com'
password - 'SreAc@d3my.2025'

1. Obtain SMTP credentials for your Outlook account (e.g. app password, SMTP host, port and TLS settings).
2. Create a Kubernetes secret containing the credentials in the `monitoring` namespace:

    ```sh
    kubectl create secret generic alertmanager-outlook-secret -n monitoring \
      --from-literal=smtp_username="sre-ibm-test@outlook.com" \
      --from-literal=smtp_password="SreAc@d3my.2025"
    ```

3. Patch the Alertmanager configuration (using Helm or `kubectl`) to reference the secret and configure the receiver.  See the Prometheus Operator documentation for details.

## Contributing

We welcome contributions of any kind—bug fixes, feature additions or documentation improvements.  Please read the [`CONTRIBUTING.md`](CONTRIBUTING.md) file for guidelines on how to get started.

## Licence

This project is licensed under the [MIT Licence](LICENSE).
