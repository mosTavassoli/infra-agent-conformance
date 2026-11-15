# Product brief

## Problem

Teams cannot safely adopt infrastructure agents based only on demos or prompt-level claims. They need reproducible evidence about diagnosis quality, data exposure, authorization boundaries, hostile operational content, safe abstention, consistency, latency, and cost.

## First user

Maintainers and platform/security engineers evaluating Kubernetes AI agents.

## First product

A local-first CLI that creates or connects to an isolated test environment, executes versioned scenarios through an agent adapter, captures evidence, performs deterministic and semantic evaluation, and exports CI-compatible reports.

## Value proposition

Run an agent against known Kubernetes failures and adversarial inputs before trusting it with real infrastructure.

## Non-goals

- Another general-purpose SRE agent
- Automatic production remediation
- A mandatory hosted service
- A mandatory observability backend
- Perfect prompt-injection detection

## Validation questions

- Do agent maintainers want regression suites independent of their own implementation?
- Do platform teams need security evidence before piloting agents?
- Which failures and reports influence an adoption decision?
- Will users run the suite repeatedly after model or policy changes?
