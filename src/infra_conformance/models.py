from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Metadata(StrictModel):
    id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)


class Target(StrictModel):
    type: Literal["kubernetes", "docker", "process"]
    profile: str


class Canary(StrictModel):
    id: str
    value: str = Field(min_length=8)
    forbidden_locations: list[str] = Field(min_length=1)


class Expectations(StrictModel):
    allowed_verbs: list[str] = Field(default_factory=list)
    forbidden_resources: list[str] = Field(default_factory=list)
    require_abstention: bool = False


class ScenarioSpec(StrictModel):
    category: Literal["agent-security", "kubernetes-reliability", "distributed-systems"]
    risk: str
    target: Target
    canaries: list[Canary] = Field(default_factory=list)
    expectations: Expectations


class Scenario(StrictModel):
    api_version: Literal["conformance.dev/v1alpha1"]
    kind: Literal["Scenario"]
    metadata: Metadata
    spec: ScenarioSpec


class Finding(StrictModel):
    check: str
    status: Literal["pass", "fail"]
    message: str
    evidence_locations: list[str] = Field(default_factory=list)


class EvaluationResult(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    scenario_id: str
    status: Literal["pass", "fail"]
    findings: list[Finding]
