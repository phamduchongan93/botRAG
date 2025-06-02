# Welcome to OmniRAG: Your Cloud-Native DevOps Showcase
---


[![CI Build Status](https://github.com/phamduchongan93/botRAG/actions/workflows/ci.yml/badge.svg)](https://github.com/phamduchongan93/botRAG/actions/workflows/ci.yml)
[![Deploy Dev Status](https://github.com/phamduchongan93/botRAG/actions/workflows/deploy-dev-gitops.yml/badge.svg)](https://github.com/phamduchongan93/botRAG/actions/workflows/deploy-dev-gitops.yml)
[![Docs Build Status](https://github.com/phamduchongan93/botRAG/actions/workflows/build-latex-requirements.yml/badge.svg)](https://github.com/phamduchongan93/botRAG/actions/workflows/build-latex-requirements.yml)

## :material-robot-happy: Project Overview

**OmniRAG** is a sophisticated Retrieval-Augmented Generation (RAG) chatbot designed not just to answer questions, but to serve as a comprehensive **DevOps showcase**. This project demonstrates the implementation of cutting-edge cloud-native practices, from microservices architecture and automated CI/CD to Infrastructure as Code and GitOps.

Our goal is to provide a clear, hands-on example of how modern applications are built, deployed, and managed with reliability, scalability, and efficiency in mind.

<div class="grid cards" markdown>
-   :material-robot-outline:{ .lg .middle } __Interactive Demo__

    Explore the live OmniRAG chatbot in action. Ask questions about DevOps, cloud-native principles, or even about this project's architecture!

    [:material-play-circle: Live Demo](https://omnirag.anpham.me/chatbot-demo) -   :material-github:{ .lg .middle } __Source Code__

    Dive into the complete codebase, Kubernetes manifests, and Terraform configurations. See the architecture and implementation details firsthand.

    [:material-code-json: GitHub Repository](https://github.com/yourgithub/omnirag-devops-showcase) -   :material-monitor-dashboard:{ .lg .middle } __Monitoring Dashboard__

    (Optional: If you set up a read-only Grafana dashboard)
    Observe real-time performance metrics, service health, and operational insights for the live deployment.

    [:material-chart-bar: View Dashboard](https://omnirag.anpham.me/dashboard) </div>

---

## :material-cloud-check: Key DevOps Principles Demonstrated

OmniRAG is built from the ground up to embody modern DevOps and cloud-native excellence. Here are the core principles you'll find demonstrated in this project:

* **Microservices Architecture:** Decomposing the RAG pipeline into independently deployable, scalable services (API Gateway, Retrieval, Generation, Ingestion).
* **Containerization (Docker):** Packaging each service into lightweight, portable containers.
* **Kubernetes Orchestration:** Automated deployment, scaling, and management of containerized applications on a cloud-managed Kubernetes cluster (AWS EKS).
* **Infrastructure as Code (IaC):** Defining and provisioning all cloud infrastructure (EKS, S3, ECR) using Terraform for reproducibility and version control.
* **CI/CD Pipelines (GitHub Actions):** Fully automated workflows for building, testing, and deploying application code and even documentation.
* **GitOps (ArgoCD):** Managing Kubernetes application deployments declaratively with Git as the single source of truth, enforced by ArgoCD.
* **Observability:** Comprehensive logging (centralized), monitoring (Prometheus, Grafana), and alerting for proactive operational insights.
* **Local Development Environment:** Providing a consistent and reproducible local Kubernetes setup (Vagrant with Libvirt/K3s) for rapid developer iteration.
* **Documentation as Code (DocOps):** Managing documentation (this site!) via Git and automated pipelines, including formal requirements in LaTeX.

---

## :material-file-document-outline: Explore the Documentation

Use the navigation on the left to delve deeper into specific aspects of the OmniRAG project:

* **[Architecture Overview](architecture.md):** Understand the high-level design and how components interact.
* **[DevOps Workflow](devops_workflow.md):** A detailed breakdown of our CI/CD pipelines, GitOps strategy, and automated processes.
* **[Setup Guide](setup_guide.md):** Instructions for setting up the project locally and deploying to your own cloud environment.
* **[Requirements Specification](requirements/omnirag_requirements_spec.pdf):** Access the formal, SEBOK-compliant requirements document (PDF).
* **[Demo Script](demo_script.md):** A guided tour for demonstrating the project's features and DevOps capabilities.

<div class="admonition abstract">
<p class="admonition-title">About the Author</p>
<p>This project is developed by **An Pham**, an aspiring DevOps Engineer with a Master's in Systems Engineering from Cal Poly Pomona and a Certified Kubernetes Administrator (CKA) certification.</p>
<p>Connect with An:</p>
<ul>
    <li>:material-linkedin: <a href="https://www.linkedin.com/in/yourlinkedin">LinkedIn Profile</a></li> <li>:material-email: <a href="mailto:anpham001@pronton.me">anpham001@pronton.me</a></li>
</ul>
</div>

---
