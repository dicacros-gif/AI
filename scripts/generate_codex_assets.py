from __future__ import annotations

from pathlib import Path

from ai_watch.manifest import AGENT_DEFINITIONS


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target_dir = root / ".codex" / "agents"
    target_dir.mkdir(parents=True, exist_ok=True)

    for role, definition in sorted(AGENT_DEFINITIONS.items()):
        body = "\n".join(
            [
                f'role = "{toml_escape(definition.role)}"',
                f'category = "{toml_escape(definition.category)}"',
                f'description = "{toml_escape(definition.description)}"',
                "phase_tags = [" + ", ".join(f'"{tag}"' for tag in definition.phase_tags) + "]",
                "required_outputs = [" + ", ".join(f'"{item}"' for item in definition.required_outputs) + "]",
                f'bias = "{toml_escape(definition.bias)}"',
                f'decisive_source_rule = "{toml_escape(definition.decisive_source_rule)}"',
                "",
            ]
        )
        (target_dir / f"{role}.toml").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()

