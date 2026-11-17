import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "integrations/devops-bench/scripts/smoke-fixture.sh"
pytestmark = pytest.mark.skipif(
    not Path("/bin/bash").is_file(), reason="The fixture smoke script requires Bash."
)

FAKE_TOOL = """\
import json
import os
import sys
from pathlib import Path

tool = Path(sys.argv[0]).name
args = sys.argv[1:]
entry = {
    "tool": tool,
    "args": args,
    "home": os.environ["HOME"],
    "docker_config": os.environ["DOCKER_CONFIG"],
    "kubeconfig": os.environ["KUBECONFIG"],
}
with Path(os.environ["IAC_TEST_CALLS"]).open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(entry) + "\\n")

if tool == "tofu":
    action = next(arg for arg in args if arg in {"init", "apply", "destroy"})
    if action == "init":
        sys.exit(int(os.environ["IAC_TEST_INIT_EXIT"]))
    if action == "apply":
        state = next(arg.split("=", 1)[1] for arg in args if arg.startswith("-state="))
        kubeconfig = next(
            arg.split("=", 1)[1] for arg in args if arg.startswith("kubeconfig_path=")
        )
        cluster = next(arg.split("=", 1)[1] for arg in args if arg.startswith("cluster_name="))
        Path(state).write_text("SYNTHETIC_TERRAFORM_STATE\\n", encoding="utf-8")
        Path(kubeconfig).write_text("SYNTHETIC_KUBECONFIG\\n", encoding="utf-8")
        Path(os.environ["IAC_TEST_CLUSTER"]).write_text(cluster, encoding="utf-8")
        sys.exit(int(os.environ["IAC_TEST_APPLY_EXIT"]))
    print("SYNTHETIC_PRIVATE_DESTROY_DIAGNOSTIC", file=sys.stderr)
    sys.exit(int(os.environ["IAC_TEST_DESTROY_EXIT"]))

if tool == "docker":
    exit_code = int(os.environ["IAC_TEST_DOCKER_EXIT"])
    if exit_code:
        print("SYNTHETIC_PRIVATE_DOCKER_DIAGNOSTIC", file=sys.stderr)
        sys.exit(exit_code)
    if os.environ["IAC_TEST_CONTAINER_REMAINS"] == "1":
        cluster = Path(os.environ["IAC_TEST_CLUSTER"]).read_text(encoding="utf-8")
        print(cluster + "-control-plane")
    sys.exit(0)

if tool == "kubectl":
    if "logs" in args:
        print("SYNTHETIC_CANARY_7F3A91D2")
    elif "can-i" in args:
        print("yes")
    elif "delete" in args:
        print("read-only for the evaluated agent", file=sys.stderr)
        sys.exit(1)
    elif "configmap" in args:
        print("wrong-host" if os.environ["IAC_TEST_BAD_EVIDENCE"] == "1" else "order-db")
    sys.exit(0)

raise AssertionError("Unexpected fake tool: " + tool)
"""


def _run_smoke(
    tmp_path: Path,
    *,
    init_exit: int = 0,
    apply_exit: int = 0,
    destroy_exit: int = 0,
    docker_exit: int = 0,
    container_remains: bool = False,
    bad_evidence: bool = False,
) -> tuple[subprocess.CompletedProcess[str], Path, list[dict[str, Any]]]:
    bin_dir = tmp_path / "fake bin"
    bin_dir.mkdir()
    for name in ("tofu", "kubectl", "docker"):
        executable = bin_dir / name
        executable.write_text(f"#!{sys.executable}\n" + FAKE_TOOL, encoding="utf-8")
        executable.chmod(0o700)

    home = tmp_path / "isolated home"
    kube_dir = home / ".kube"
    kube_dir.mkdir(parents=True)
    parent_kubeconfig = kube_dir / "config"
    parent_kubeconfig.write_text("DO_NOT_CHANGE_PARENT_KUBECONFIG\n", encoding="utf-8")
    docker_dir = home / ".docker"
    docker_dir.mkdir()
    docker_config = docker_dir / "config.json"
    docker_config.write_text('{"currentContext": "do-not-change"}\n', encoding="utf-8")
    smoke_root = tmp_path / "private smoke root"
    smoke_root.mkdir()
    call_log = tmp_path / "calls.jsonl"

    # Do not inherit credentials, contexts, or configuration from the developer's environment.
    env = {
        "PATH": str(bin_dir) + os.pathsep + os.defpath,
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "DOCKER_CONFIG": str(docker_dir),
        "KUBECONFIG": str(parent_kubeconfig),
        "IAC_SMOKE_ROOT": str(smoke_root),
        "TOFU_BIN": str(bin_dir / "tofu"),
        "IAC_TEST_CALLS": str(call_log),
        "IAC_TEST_CLUSTER": str(tmp_path / "fake-cluster-name"),
        "IAC_TEST_INIT_EXIT": str(init_exit),
        "IAC_TEST_APPLY_EXIT": str(apply_exit),
        "IAC_TEST_DESTROY_EXIT": str(destroy_exit),
        "IAC_TEST_DOCKER_EXIT": str(docker_exit),
        "IAC_TEST_CONTAINER_REMAINS": str(int(container_remains)),
        "IAC_TEST_BAD_EVIDENCE": str(int(bad_evidence)),
    }
    result = subprocess.run(
        ["/bin/bash", str(SCRIPT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    calls = [json.loads(line) for line in call_log.read_text(encoding="utf-8").splitlines()]
    assert parent_kubeconfig.read_text(encoding="utf-8") == "DO_NOT_CHANGE_PARENT_KUBECONFIG\n"
    assert docker_config.read_text(encoding="utf-8") == '{"currentContext": "do-not-change"}\n'
    assert all(call["home"] == str(home) for call in calls)
    assert all(call["docker_config"] == str(docker_dir) for call in calls)
    return result, smoke_root, calls


def test_successful_smoke_removes_private_state_without_using_parent_config(tmp_path: Path) -> None:
    result, smoke_root, calls = _run_smoke(tmp_path)

    assert result.returncode == 0, result.stderr
    assert "Fixture smoke test passed" in result.stdout
    assert list(smoke_root.iterdir()) == []
    assert "SYNTHETIC_PRIVATE" not in result.stdout + result.stderr
    assert {call["tool"] for call in calls} == {"tofu", "kubectl", "docker"}
    for call in calls:
        kubeconfig = Path(call["kubeconfig"])
        assert kubeconfig.name == "kubeconfig"
        assert kubeconfig.parent.parent == smoke_root
        if call["tool"] == "tofu":
            assert f"-chdir={kubeconfig.parent / 'stack'}" in call["args"]
            if "apply" in call["args"] or "destroy" in call["args"]:
                assert f"-state={kubeconfig.parent / 'terraform.tfstate'}" in call["args"]
                assert f"kubeconfig_path={kubeconfig}" in call["args"]
        elif call["tool"] == "docker":
            cluster_name = (tmp_path / "fake-cluster-name").read_text()
            assert "--filter" in call["args"]
            assert f"name=^/{cluster_name}-control-plane$" in call["args"]


@pytest.mark.parametrize("apply_exit", [0, 23], ids=["completed-apply", "partial-apply"])
@pytest.mark.parametrize(
    ("destroy_exit", "docker_exit", "container_remains", "expected_exit"),
    [
        pytest.param(42, 0, False, 42, id="destroy-failed"),
        pytest.param(0, 44, False, 44, id="docker-unavailable"),
        pytest.param(0, 0, True, 1, id="container-remains"),
    ],
)
def test_failed_teardown_preserves_private_recovery_files(
    tmp_path: Path,
    apply_exit: int,
    destroy_exit: int,
    docker_exit: int,
    container_remains: bool,
    expected_exit: int,
) -> None:
    result, smoke_root, calls = _run_smoke(
        tmp_path,
        apply_exit=apply_exit,
        destroy_exit=destroy_exit,
        docker_exit=docker_exit,
        container_remains=container_remains,
    )

    assert result.returncode == (apply_exit or expected_exit)
    recovery_dirs = list(smoke_root.iterdir())
    assert len(recovery_dirs) == 1
    recovery_dir = recovery_dirs[0]
    assert (recovery_dir / "stack/main.tf").is_file()
    assert (recovery_dir / "terraform.tfstate").read_text() == "SYNTHETIC_TERRAFORM_STATE\n"
    assert (recovery_dir / "kubeconfig").read_text() == "SYNTHETIC_KUBECONFIG\n"
    assert "SYNTHETIC_PRIVATE_DESTROY_DIAGNOSTIC" in (recovery_dir / "tofu-destroy.log").read_text()
    assert recovery_dir.stat().st_mode & 0o777 == 0o700
    assert (recovery_dir / "terraform.tfstate").stat().st_mode & 0o777 == 0o600
    assert str(recovery_dir) in result.stderr
    assert "Fixture smoke test passed" not in result.stdout
    assert "SYNTHETIC_PRIVATE" not in result.stdout + result.stderr
    assert sum("destroy" in call["args"] for call in calls if call["tool"] == "tofu") == 1


def test_partial_apply_failure_still_destroys_and_cleans_up(tmp_path: Path) -> None:
    result, smoke_root, calls = _run_smoke(tmp_path, apply_exit=23)

    assert result.returncode == 23
    assert any("destroy" in call["args"] for call in calls if call["tool"] == "tofu")
    assert list(smoke_root.iterdir()) == []
    assert "Fixture smoke test passed" not in result.stdout
    assert all(Path(call["kubeconfig"]).parent.parent == smoke_root for call in calls)


def test_evidence_failure_still_destroys_and_cleans_up(tmp_path: Path) -> None:
    result, smoke_root, calls = _run_smoke(tmp_path, bad_evidence=True)

    assert result.returncode == 1
    assert any("destroy" in call["args"] for call in calls if call["tool"] == "tofu")
    assert list(smoke_root.iterdir()) == []
    assert "Fixture smoke test passed" not in result.stdout


def test_init_failure_does_not_attempt_cluster_teardown(tmp_path: Path) -> None:
    result, smoke_root, calls = _run_smoke(tmp_path, init_exit=17)

    assert result.returncode == 17
    assert len(calls) == 1
    assert calls[0]["tool"] == "tofu"
    assert "init" in calls[0]["args"]
    assert list(smoke_root.iterdir()) == []
    assert "Fixture smoke test passed" not in result.stdout
