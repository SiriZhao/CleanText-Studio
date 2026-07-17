"""Keep community-facing launch material complete and professionally scoped."""

from pathlib import Path

ROOT = Path(__file__).parents[2]
LAUNCH = ROOT / "docs" / "launch"
REQUIRED = {
    "README.md",
    "github-launch.md",
    "reddit-launch.md",
    "hackernews-launch.md",
    "producthunt-launch.md",
    "twitter-launch.md",
    "community-list.md",
    "release-v1.5.md",
}


def test_launch_kit_is_complete_and_uses_the_project_positioning() -> None:
    assert {path.name for path in LAUNCH.glob("*.md")} >= REQUIRED
    content = "\n".join(path.read_text(encoding="utf-8") for path in LAUNCH.glob("*.md"))
    assert "privacy-first" in content.casefold()
    assert "local-first" in content.casefold()
    assert "document formatting" in content.casefold()


def test_discussion_templates_and_label_guide_exist() -> None:
    templates = ROOT / ".github" / "DISCUSSION_TEMPLATE"
    assert {path.name for path in templates.glob("*.md")} == {"ideas.md", "help.md", "showcase.md"}
    labels = (ROOT / ".github" / "labels.md").read_text(encoding="utf-8")
    assert "good first issue" in labels
    assert "help wanted" in labels
