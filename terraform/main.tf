terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.11.0"
    }
  }
}

# Kubernetes provider using local kubeconfig
provider "kubernetes" {
  config_path = var.kubeconfig_path
}

# Helm provider — correct syntax for new versions
provider "helm" {
  kubernetes = {
    config_path = var.kubeconfig_path
  }
}

# Variables
variable "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "app_image_repository" {
  description = "Docker image repository for the application"
  type        = string
  default     = "little-ragnar/sports-store-order-service"
}

variable "app_image_tag" {
  description = "Docker image tag for the application"
  type        = string
  default     = "latest"
}

# Helm release for the sports store application
resource "helm_release" "sports_store_app" {
  name             = "sports-store-app"
  chart            = "../charts/sports-store-app"
  namespace        = "sports-store"
  create_namespace = true

  # The image repo and tag now come ONLY from this YAML file.
  # It avoids incompatibilities with "set" blocks (which your provider doesn't support).
  values = [
    file("${path.module}/values/sports-store-app-values.yaml")
  ]
}