import json
from pathlib import Path
from typing import Annotated

import typer
from opentelemetry import trace
from rich.console import Console

from infra_conformance import __version__
from infra_conformance.evaluator import evaluate_canary_leakage
from infra_conformance.loader import load_scenario

app = typer.Typer(no_args_is_help=True, help="Evaluate infrastructure agents safely.")
console = Console()
tracer = trace.get_tracer("infra_conformance.cli")


def _parse_artifacts(items: list[str]) -> dict[str, str]:
    artifacts: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise typer.BadParameter("Artifacts must use LOCATION=PATH syntax.")
        location, raw_path = item.split("=", 1)
        path = Path(raw_path)
        if not path.is_file():
            raise typer.BadParameter(f"Artifact does not exist: {path}")
        artifacts[location] = path.read_text(encoding="utf-8")
    return artifacts


@app.command()
def version() -> None:
    """Print the CLI version."""
    console.print(__version__)


@app.command()
def validate(scenario_path: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]) -> None:
    """Validate a scenario against the versioned contract."""
    with tracer.start_as_current_span("scenario.validate"):
        scenario = load_scenario(scenario_path)
    console.print(f"[green]Valid[/green] {scenario.metadata.id}: {scenario.metadata.title}")


@app.command()
def evaluate(
    scenario_path: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    artifact: Annotated[
        list[str] | None,
        typer.Option("--artifact", "-a", help="Artifact as LOCATION=PATH; repeat as needed."),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Optional JSON result path."),
    ] = None,
) -> None:
    """Run deterministic leakage checks against captured artifacts."""
    with tracer.start_as_current_span("scenario.evaluate"):
        scenario = load_scenario(scenario_path)
        artifacts = _parse_artifacts(artifact or [])
        result = evaluate_canary_leakage(scenario, artifacts)
        rendered = json.dumps(result.model_dump(), indent=2)
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered + "\n", encoding="utf-8")

    color = "green" if result.status == "pass" else "red"
    console.print(f"[{color}]{result.status.upper()}[/{color}] {result.scenario_id}")
    for finding in result.findings:
        console.print(f"- {finding.status.upper()}: {finding.message}")
    if not output:
        console.print(rendered)
    if result.status == "fail":
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
