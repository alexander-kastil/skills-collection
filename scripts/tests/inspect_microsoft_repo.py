#!/usr/bin/env python3
"""
Inspect Microsoft Skills Repository Structure
Shows the repository layout, skill locations, and what flat names would be generated.
"""

import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

MS_REPO = "https://github.com/microsoft/skills.git"


def extract_skill_name(skill_md_path: Path) -> Optional[str]:
    """Extract the 'name' field from SKILL.md YAML frontmatter."""
    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except Exception:
        return None

    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return None

    for line in fm_match.group(1).splitlines():
        match = re.match(r"^name:\s*(.+)$", line)
        if match:
            value = match.group(1).strip().strip("\"'")
            if value:
                return value
    return None


def inspect_repo():
    """Inspect the Microsoft skills repository structure."""
    print("🔍 Inspecting Microsoft Skills Repository Structure")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        print("\n1️⃣ Cloning repository...")
        subprocess.run(
            ["git", "clone", "--depth", "1", MS_REPO, str(temp_path)],
            check=True,
            capture_output=True,
        )

        # Find all SKILL.md files
        all_skill_mds = list(temp_path.rglob("SKILL.md"))
        print(f"\n2️⃣ Total SKILL.md files found: {len(all_skill_mds)}")

        # Show flat name mapping
        print(f"\n3️⃣ Flat Name Mapping (frontmatter 'name' → directory name):")
        print("-" * 60)

        names_seen: dict[str, list[str]] = {}

        for skill_md in sorted(all_skill_mds, key=lambda p: str(p)):
            try:
                rel = skill_md.parent.relative_to(temp_path)
            except ValueError:
                rel = skill_md.parent

            name = extract_skill_name(skill_md)
            display_name = name if name else f"(no name → ms-{'-'.join(rel.parts[1:])})"

            print(f"  {rel} → {display_name}")

            effective_name = name if name else f"ms-{'-'.join(rel.parts[1:])}"
            if effective_name not in names_seen:
                names_seen[effective_name] = []
            names_seen[effective_name].append(str(rel))

        # Collision check
        collisions = {n: paths for n, paths in names_seen.items()
                      if len(paths) > 1}
        if collisions:
            print(f"\n4️⃣ ⚠️  Name Collisions Detected ({len(collisions)}):")
            for name, paths in collisions.items():
                print(f"  '{name}':")
                for p in paths:
                    print(f"    - {p}")
        else:
            print(
                f"\n4️⃣ ✅ No name collisions - all {len(names_seen)} names are unique!")

        print("\n✨ Inspection complete!")


if __name__ == "__main__":
    try:
        inspect_repo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
