---

# OmniRAG: Project Directory Structure (WIP)

This document details the logical organization of the `omnirag-devops-showcase` project. This structure is designed to promote **clarity, maintainability, and scalability** for a cloud-native application, emphasizing **microservices, Kubernetes, CI/CD, Infrastructure as Code (IaC), and GitOps principles**.

```
omnirag-devops-showcase/
├── .github/
│   └── workflows/
│       ├── ci.yml                     # GitHub Actions: Builds, tests, and pushes Docker images to a registry.
│       ├── deploy-dev-gitops.yml      # GitHub Actions: Updates Dev Kubernetes manifests in Git for ArgoCD.
│       ├── deploy-prod-gitops.yml     # GitHub Actions: Updates Prod Kubernetes manifests in Git for ArgoCD (with approval).
│       ├── terraform-apply.yml        # GitHub Actions: Manages underlying cloud infrastructure via Terraform.
│       ├── reusable-build-push.yml    # (Optional) Reusable workflow to build and push a single service image.
│       └── reusable-update-k8s-manifest.yml # (Optional) Reusable workflow to update image tags in K8s manifests.
├── terraform/
│   ├── modules/                       # Reusable Terraform modules for common cloud resources.
│   │   ├── eks-cluster/               # Defines the EKS cluster and node groups.
│   │   ├── rds-pgvector/              # Defines managed PostgreSQL with `pgvector` (if used).
│   │   ├── s3-bucket/                 # Defines S3 bucket for the knowledge base.
│   │   ├── ecr-repo/                  # Defines ECR repositories for Docker images.
│   │   └── network/                   # Defines VPC, subnets, and security groups.
│   ├── environments/                  # Environment-specific Terraform configurations.
│   │   ├── dev/                       # Configuration for the development cloud environment.
│   │   │   └── main.tf
│   │   └── prod/                      # Configuration for the production cloud environment.
│   │       └── main.tf
│   └── README.md                      # Documentation on Terraform usage.
├── services/
│   ├── api-gateway-service/           # FastAPI/Flask application: Entry point for user requests.
│   │   ├── app/                       # Core application logic.
│   │   │   └── main.py
│   │   ├── Dockerfile                 # Docker build instructions for this service.
│   │   ├── requirements.txt           # Python dependencies for this service.
│   │   └── tests/                     # Unit and integration tests for this service.
│   ├── retrieval-service/             # FastAPI/Flask application: Embeds queries, retrieves context from Vector DB.
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── generation-service/            # FastAPI/Flask application: Prompts LLM with query and context.
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── ingestion-service/             # Python script/app: Loads, chunks, and embeds knowledge base documents.
│   │   ├── app/
│   │   │   └── ingest.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   └── README.md                      # Overview of the microservices.
├── kubernetes/
│   ├── base/                          # Base Kubernetes manifests, common across all environments.
│   │   ├── omnirag-namespace.yaml     # Defines the Kubernetes namespace.
│   │   ├── ingress.yaml               # Base Ingress definition for external access.
│   │   ├── kustomization.yaml         # Kustomize base configuration.
│   │   ├── secrets-template.yaml      # Template for Kubernetes Secrets (actual secrets injected via CI/CD or external secrets).
│   │   ├── common-configmaps.yaml     # Common configuration values.
│   │   ├── api-gateway-service/       # Base Deployment, Service, and HPA for API Gateway.
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── hpa.yaml
│   │   ├── retrieval-service/         # Base Deployment, Service, and HPA for Retrieval Service.
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── hpa.yaml
│   │   ├── generation-service/        # Base Deployment, Service, and HPA for Generation Service.
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── hpa.yaml
│   │   └── ingestion-service/         # Base Kubernetes Job and ConfigMap for Ingestion Service.
│   │       ├── job.yaml
│   │       └── configmap.yaml
│   ├── overlays/                      # Environment-specific Kubernetes overlays using Kustomize.
│   │   ├── dev/                       # Development environment overrides.
│   │   │   ├── kustomization.yaml     # Kustomize configuration for dev.
│   │   │   └── patches/               # Specific patches for dev (e.g., lower replicas, dev ingress).
│   │   │       └── api-gateway-patch.yaml
│   │   └── prod/                      # Production environment overrides.
│   │       ├── kustomization.yaml     # Kustomize configuration for prod.
│   │       └── patches/               # Specific patches for prod (e.g., higher replicas, prod ingress, resource limits).
│   │           └── api-gateway-patch.yaml
│   ├── argo-apps/                     # ArgoCD Application definitions (if managing Argo itself here).
│   │   ├── omnirag-dev-app.yaml       # ArgoCD Application for the dev environment.
│   │   └── omnirag-prod-app.yaml      # ArgoCD Application for the prod environment.
│   └── README.md                      # Documentation on Kubernetes manifests and GitOps setup.
├── environments/
│   ├── local/                         # Local development environment setup.
│   │   ├── Vagrantfile                # Vagrantfile for provisioning a local Kubernetes cluster (e.g., K3s via Libvirt).
│   │   ├── README.md                  # Instructions for setting up the local environment.
│   │   └── setup_local_k8s.sh         # (Optional) Script to install local K8s distro and configure `kubectl`.
│   └── README.md                      # Overview of environment configurations.
├── knowledge_base/                    # Sample raw knowledge base documents for ingestion.
│   └── docs/                          # Example document types.
│       ├── getting_started.md
│       ├── troubleshooting.pdf
│       └── product_manual.txt
├── docs/                              # General project documentation, diagrams, and demo scripts.
│   ├── architecture.md                # Detailed architecture diagrams.
│   ├── devops_workflow.md             # In-depth explanation of CI/CD and GitOps flow.
│   ├── setup_guide.md                 # End-to-end setup instructions.
│   └── demo_script.md                 # Steps for demonstrating the project.
├── .gitignore                         # Specifies intentionally untracked files to ignore.
└── README.md                          # The main project overview.
```

# Local Development Environment Setup

This directory contains the necessary files and scripts to set up a consistent local Kubernetes environment for developing and testing OmniRAG microservices.

## Technologies Used:

* **Vagrant:** For provisioning a lightweight virtual machine.
* **VirtualBox (or other Vagrant provider):** The virtualization software.
* **[Kubernetes Distribution]:** (e.g., K3s, MicroK8s, or Minikube) running inside the Vagrant VM.

## Prerequisites:

1.  **Vagrant:** [Install Vagrant](https://www.vagrantup.com/downloads)
2.  **VirtualBox:** [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) (or your chosen Vagrant provider)
3.  **`kubectl`:** [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (if you want to interact with the local cluster from your host machine)

## Setup Instructions:

1.  Navigate to this directory:
    ```bash
    cd omnirag-devops-showcase/environments/local
    ```
2.  Start the Vagrant VM and provision Kubernetes:
    ```bash
    vagrant up
    ```
    This process may take some time as it downloads the VM image and installs Kubernetes.

3.  (Optional) Configure `kubectl` on your host to interact with the local cluster:
    * The `Vagrantfile` should ideally place the `kubeconfig` file on the host or provide instructions to retrieve it.
    * Example for K3s inside Vagrant:
        ```bash
        vagrant ssh -c "sudo cat /etc/rancher/k3s/k3s.yaml" > ~/.kube/config_omnirag_local
        # Then, set KUBECONFIG:
        export KUBECONFIG=$KUBECONFIG:~/.kube/config_omnirag_local
        kubectl config use-context default # Or the context name provided by k3s
        ```
    * **Always verify the context to avoid accidentally targeting a production cluster!**
        ```bash
        kubectl config current-context
        ```

4.  Verify Kubernetes cluster is running:
    ```bash
    kubectl get nodes
    kubectl get pods -n kube-system
    ```

## Developing with Skaffold:

Once your local Kubernetes cluster is up, you can use [Skaffold](link-to-your-skaffold-docs-or-skaffold.yaml) to iterate quickly on your microservices.

1.  Ensure Skaffold is [installed](https://skaffold.dev/docs/install/).
2.  From the project root (`omnirag-devops-showcase/`), run:
    ```bash
    skaffold dev --kube-context <your-local-kube-context> # e.g., --kube-context k3s-default
    ```
    This will automatically build your service images, deploy them to your local Kubernetes, and stream logs.

## Teardown:

To stop and remove the local VM:
```bash
vagrant destroy -f
```
## Environments and Deployment Strategy

- Multi-branch model (dev → qa → main → prod)
- GitOps overlays via Kustomize
- ArgoCD syncs from environment-specific overlays
- Infrastructure managed separately via Terraform

See [`docs/devops_workflow.md`](./docs/devops_workflow.md) for details.

## Cost Estimate Analysis for Production
| Environment    | Infra           | Autoscaling         | Cost     |
| -------------- | --------------- | ------------------- | -------- |
| `local`        | Vagrant + K3s   | Manual              | Free     |
| `eks-anywhere` | On-prem / VMs   | Custom script / CA  | Free-ish |
| `dev`          | EKS + Karpenter | Dynamic (Karpenter) | \$       |
| `prod`         | EKS + ASGs (Auto Scaling Group)      | Controlled          | \$\$     |

