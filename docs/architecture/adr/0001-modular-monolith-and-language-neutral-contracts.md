# ADR 0001: Modular monolith and language-neutral contracts

**Status:** Accepted  
**Date:** 2026-11-15

## Context

The project needs rapid iteration in the AI evaluation ecosystem while preserving the option to add Kubernetes-native or .NET components later. Starting with microservices or several languages would increase operational and contribution cost before requirements are known.

## Decision

- Implement the first release as a Python modular monolith.
- Define scenarios, results, and adapter messages with versioned JSON Schema.
- Use local process or HTTP boundaries for external adapters.
- Package external adapters as OCI images when portability is required.

## Consequences

- Initial development and testing remain simple.
- Public contracts are not tied to Python.
- Some future high-throughput components may be rewritten without changing scenario authorship.
- Contract compatibility must be tested and documented.
