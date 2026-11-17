variable "infra_provider" {
  type        = string
  description = "DevOps Bench provider name; this bounded fixture supports KinD only."
  default     = "kind"

  validation {
    condition     = var.infra_provider == "kind"
    error_message = "The adversarial telemetry fixture supports only the kind provider."
  }
}

variable "project_id" {
  type        = string
  description = "Local project marker supplied by the DevOps Bench KinD provider."
  default     = "local-kind"
}

variable "cluster_name" {
  type        = string
  description = "Run-unique KinD cluster name."
  default     = "infra-conformance-security"
}

variable "location" {
  type        = string
  description = "Local location marker."
  default     = "local"
}

variable "kubeconfig_path" {
  type        = string
  description = "Path where KinD writes the run-scoped kubeconfig."
  default     = "~/.kube/config"
}

variable "node_image" {
  type        = string
  description = "Pinned Kubernetes node image with ValidatingAdmissionPolicy v1 support."
  default     = "kindest/node:v1.30.0@sha256:047357ac0cfea04663786a612ba1eaba9702bef25227a794b52890dd8bcd692e"
}
