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

provider "kubernetes" {
  # Use local kubeconfig by default.  Adjust the path if necessary.
  config_path = var.kubeconfig_path
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig_path
  }
}

variable "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "app_image_repository" {
  description = "Docker image repository for the application"
  type        = string
  default     = "sports-store-order-service"
}

variable "app_image_tag" {
  description = "Docker image tag for the application"
  type        = string
  default     = "latest"
}

# Helm release for the sports store application
resource "helm_release" "sports_store_app" {
  name       = "sports-store-app"
  chart      = "../charts/sports-store-app"
  namespace  = "sports-store"
  create_namespace = true

  set {
    name  = "image.repository"
    value = var.app_image_repository
  }
  set {
    name  = "image.tag"
    value = var.app_image_tag
  }

  # Include additional values from a YAML file.  This allows you to override
  # Helm values without editing the chart itself.
  values = [
    file("${path.module}/values/sports-store-app-values.yaml")
  ]
}