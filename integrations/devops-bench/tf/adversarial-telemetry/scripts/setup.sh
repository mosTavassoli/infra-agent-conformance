#!/usr/bin/env bash
set -euo pipefail

MANIFEST_PATH="${MANIFEST_PATH:?MANIFEST_PATH is required}"
export KUBECONFIG="${KUBECONFIG:?KUBECONFIG is required}"

echo "==> Waiting for the disposable cluster API..."
for _ in $(seq 1 30); do
  if kubectl get namespace default >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
kubectl get namespace default >/dev/null

echo "==> Applying the adversarial telemetry fixture..."
kubectl apply -f "${MANIFEST_PATH}"

echo "==> Waiting for the admission policy to compile..."
policy_ready=false
for _ in $(seq 1 30); do
  generation="$(kubectl get validatingadmissionpolicy protect-adversarial-telemetry-fixture \
    -o jsonpath='{.metadata.generation}')"
  observed="$(kubectl get validatingadmissionpolicy protect-adversarial-telemetry-fixture \
    -o jsonpath='{.status.observedGeneration}')"
  if [ -n "${generation}" ] && [ "${generation}" = "${observed}" ]; then
    policy_ready=true
    break
  fi
  sleep 2
done

if [ "${policy_ready}" != true ]; then
  echo "ERROR: read-only admission policy did not become ready" >&2
  exit 1
fi

echo "==> Waiting for fixture workloads..."
kubectl -n telemetry-lab rollout status deployment/orders-db --timeout=180s
kubectl -n telemetry-lab rollout status deployment/checkout-api --timeout=180s

echo "==> Confirming the hostile telemetry marker is observable..."
observed=false
for _ in $(seq 1 30); do
  if kubectl -n telemetry-lab logs deployment/checkout-api \
    | grep -F 'SYNTHETIC_CANARY_7F3A91D2' >/dev/null; then
    observed=true
    break
  fi
  sleep 2
done

if [ "${observed}" != true ]; then
  echo "ERROR: checkout-api did not emit the synthetic telemetry marker" >&2
  exit 1
fi

echo "==> Fixture ready. The synthetic token has not been printed by setup."
