from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def restore_artifact_dir(artifact_dir: Path, repo_root: Path) -> None:
    manifest_path = artifact_dir / "run_manifest.json"
    if not manifest_path.exists():
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    phase_root = repo_root / manifest["phaseRoot"]
    if phase_root.exists():
        shutil.rmtree(phase_root)
    phase_root.mkdir(parents=True, exist_ok=True)

    for item in artifact_dir.iterdir():
        target = phase_root / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root)
    repo_root = Path(args.repo_root).resolve()
    if not artifact_root.exists():
        return

    for manifest_path in sorted(artifact_root.rglob("run_manifest.json")):
        restore_artifact_dir(manifest_path.parent, repo_root)


if __name__ == "__main__":
    main()
