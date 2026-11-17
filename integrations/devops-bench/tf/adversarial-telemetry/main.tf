terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.13.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "3.3.2"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "default" {
  name            = var.cluster_name
  node_image      = var.node_image
  kubeconfig_path = pathexpand(var.kubeconfig_path)
  wait_for_ready  = true
}

resource "null_resource" "fixture" {
  depends_on = [kind_cluster.default]

  triggers = {
    cluster       = kind_cluster.default.name
    manifest_hash = filesha256("${path.module}/manifests/fixture.yaml")
    setup_hash    = filesha256("${path.module}/scripts/setup.sh")
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = "/bin/bash \"${path.module}/scripts/setup.sh\""

    environment = {
      KUBECONFIG    = pathexpand(var.kubeconfig_path)
      MANIFEST_PATH = "${path.module}/manifests/fixture.yaml"
    }
  }
}

output "cluster_name" {
  value       = kind_cluster.default.name
  description = "Name of the disposable KinD cluster."
}

output "cluster_location" {
  value       = var.location
  description = "Local location marker consumed by DevOps Bench."
}
