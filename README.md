# Kubernetes CI/CD Deployment Project

## Project Overview

This project involves the implementation of a cloud-native CI/CD pipeline to deploy and manage two microservices—Gatekeeper and Processor—within Kubernetes clusters on Google Kubernetes Engine (GKE). The project leverages Terraform for infrastructure automation and GCP Cloud Build for CI/CD processes.

## Key Features

- **Microservices Deployment**: The project includes two microservices—Gatekeeper and Processor—containerized using Docker and deployed on GKE.
- **CI/CD Automation**: Automated build and deployment using GCP Cloud Build and Kubernetes manifests.
- **Infrastructure as Code (IaC)**: Terraform is used for provisioning and managing GKE clusters, ensuring consistent and reproducible infrastructure.
- **Persistent Storage**: Configured persistent volumes in GKE to store and manage data for the microservices.

## Technologies Used

- **Kubernetes**: For orchestrating and managing the containerized microservices.
- **Docker**: To containerize the Gatekeeper and Processor services.
- **Terraform**: For automating the creation and management of GKE clusters.
- **Google Cloud Platform (GCP)**: Utilizing Cloud Build for CI/CD and GKE for container orchestration.
- **Python & Bash**: For scripting and automation of tasks.
- **Prometheus & Grafana**: For monitoring and logging (if applicable).

## Project Structure

```plaintext

├── Gatekeeper/
│   ├── Dockerfile
│   ├── GateKeeper.py
│   ├── cloudbuild.yaml
│   ├── requirements.txt
│   └── kubernetes-file/
│       ├── gatekeeper-deployment.yaml
│       ├── gatekeeper-service.yaml
│       └── pvc.yaml
├── Processor/
│   ├── Dockerfile
│   ├── Processor.py
│   ├── cloudbuild.yaml
│   ├── requirements.txt
│   └── kubernetes-file/
│       ├── processor-deployment.yaml
│       ├── processor-service.yaml
└── Terraform/
│       ├── main.tf
│       └── terraform.tfvars
```

## Setup Instructions

### Prerequisites

- **Google Cloud Account**: Ensure you have access to GCP with billing enabled.
- **Terraform Installed**: Terraform should be installed on your local machine or GCP Cloud Shell.
- **Docker Installed**: Docker must be installed locally for building and pushing images.
- **kubectl Installed**: kubectl should be installed to interact with the GKE cluster.

### Steps to Deploy

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Yash-javiya/Kubernetes-CI-CD-Deployment.git
    cd kubernetes-cicd-deployment
    ```

2. **Build and Push Docker Images**:

    ```bash
    cd K8s/Gatekeeper
    docker build -t gcr.io/your-project-id/gatekeeper:latest .
    docker push gcr.io/your-project-id/gatekeeper:latest

    cd ../Processor
    docker build -t gcr.io/your-project-id/processor:latest .
    docker push gcr.io/your-project-id/processor:latest
    ```

3. **Provision GKE Cluster using Terraform**:

    ```bash
    cd K8s/Terraform
    terraform init
    terraform apply
    ```

4. **Deploy Microservices to GKE**:

    ```bash
    kubectl apply -f ../Gatekeeper/kubernetes-file/
    kubectl apply -f ../Processor/kubernetes-file/
    ```

5. **Monitor the Deployment**:

    ```bash
    kubectl get pods
    kubectl logs <pod-name>
    ```

## Usage

- **Accessing the Microservices**: Once deployed, the microservices can be accessed via the external IP address provided by the GKE services.
- **Monitoring**: Use tools like Prometheus and Grafana (if configured) to monitor cluster and application performance.

## Lessons Learned

This project enhanced my skills in Kubernetes, Terraform, and CI/CD automation. It provided hands-on experience with containerizing applications and deploying them in a scalable, cloud-native environment.

## Future Enhancements

- **Automated Scaling**: Implement horizontal pod autoscaling to dynamically manage load.
- **Enhanced Security**: Integrate additional security measures, such as network policies and secret management.
- **Advanced Monitoring**: Expand monitoring capabilities with custom metrics and alerts.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Professor Rob Hawkey for the foundational work that inspired this project.
