from diagrams import Diagram, Cluster
from diagrams.aws.network import Route53
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.k8s.compute import Pod, Ingress
from diagrams.k8s.ecosystem import KubeVirt
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.database import Postgresql # For on-prem vector DB
from diagrams.generic.network import VPN # For data sync

with Diagram("OmniRAG Hybrid Cloud Architecture", show=False, direction="LR"): # show=False prevents opening after generation
    internet = Internet("User")

    dns = Route53("DNS (Route 53)")

    with Cluster("On-Premises Data Center"):
        on_prem_ingress = Ingress("On-Prem K8s Ingress")
        on_prem_k8s_node = Server("On-Prem Kubernetes Node") # Represents the K8s cluster
        on_prem_app_pods = Pod("OmniRAG App Pods")
        on_prem_vector_db = Postgresql("On-Prem Vector DB") # Placeholder for local DB
        local_kb = S3("Local KB / MinIO") # Placeholder for local object storage

        on_prem_k8s_node - on_prem_app_pods
        on_prem_app_pods - on_prem_vector_db
        on_prem_app_pods - local_kb

    with Cluster("AWS Cloud"):
        eks_ingress = Ingress("EKS K8s Ingress (ALB)")
        eks_k8s = EC2("EKS Kubernetes Cluster") # Represents EKS Nodes/Control Plane
        eks_app_pods = Pod("OmniRAG App Pods")
        rds_vector_db = RDS("AWS RDS PGVector")
        s3_kb = S3("AWS S3 Knowledge Base")

        eks_k8s - eks_app_pods
        eks_app_pods - rds_vector_db
        eks_app_pods - s3_kb

    # Flow
    internet >> dns
    dns >> on_prem_ingress
    dns >> eks_ingress

    on_prem_ingress >> on_prem_k8s_node
    eks_ingress >> eks_k8s

    # Data Sync (conceptual)
    on_prem_vector_db - VPN("DB Replication") - rds_vector_db
    local_kb - VPN("KB Sync") - s3_kb

    # Health Checks (conceptual)
    dns >> on_prem_ingress # Implied health check from DNS
    dns >> eks_ingress # Implied health check from DNS
