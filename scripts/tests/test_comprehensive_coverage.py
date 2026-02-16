#!/usr/bin/env python3
"""
Test Script: Verify Microsoft Skills Sync Coverage and Flat Name Uniqueness
Ensures all skills are captured and no directory name collisions exist.
"""

import re
import subprocess
import tempfile
from pathlib import Path
from collections import defaultdict

MS_REPO = "https://github.com/microsoft/skills.git"


def extract_skill_name(skill_md_path: Path) -> str | None:
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


def analyze_skill_locations():
    """
    Comprehensive analysis of all skill locations in Microsoft repo.
    Verifies flat name uniqueness and coverage.
    """
    print("🔬 Comprehensive Skill Coverage & Uniqueness Analysis")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        print("\n1️⃣ Cloning repository...")
        subprocess.run(
            ["git", "clone", "--depth", "1", MS_REPO, str(temp_path)],
            check=True,
            capture_output=True,
        )

        # Find ALL SKILL.md files
        all_skill_files = list(temp_path.rglob("SKILL.md"))
        print(f"\n2️⃣ Total SKILL.md files found: {len(all_skill_files)}")

        # Categorize by location
        location_types = defaultdict(list)
        for skill_file in all_skill_files:
            path_str = str(skill_file)
            if ".github/skills" in path_str:
                location_types["github_skills"].append(skill_file)
            elif ".github/plugins" in path_str:
                location_types["github_plugins"].append(skill_file)
            elif "/skills/" in path_str:
                location_types["skills_dir"].append(skill_file)
            else:
                location_types["other"].append(skill_file)

        print("\n3️⃣ Skills by Location Type:")
        for loc_type, files in sorted(location_types.items()):
            print(f"  📍 {loc_type}: {len(files)} skills")

        # Flat name uniqueness check
        print("\n4️⃣ Flat Name Uniqueness Check:")
        print("-" * 60)

        name_map: dict[str, list[str]] = {}
        missing_names = []

        for skill_file in all_skill_files:
            try:
                rel = skill_file.parent.relative_to(temp_path)
            except ValueError:
                rel = skill_file.parent

            name = extract_skill_name(skill_file)
            if not name:
                missing_names.append(str(rel))
                # Generate fallback
                parts = [p for p in rel.parts if p not in (
                    ".github", "skills", "plugins")]
                name = "ms-" + "-".join(parts) if parts else str(rel)

            if name not in name_map:
                name_map[name] = []
            name_map[name].append(str(rel))

        # Report results
        collisions = {n: paths for n, paths in name_map.items()
                      if len(paths) > 1}
        unique_names = {n: paths for n,
                        paths in name_map.items() if len(paths) == 1}

        print(f"\n  ✅ Unique names: {len(unique_names)}")

        if missing_names:
            print(
                f"\n  ⚠️  Skills missing frontmatter 'name' ({len(missing_names)}):")
            for path in missing_names[:5]:
                print(f"     - {path}")
            if len(missing_names) > 5:
                print(f"     ... and {len(missing_names) - 5} more")

        if collisions:
            print(f"\n  ❌ Name collisions ({len(collisions)}):")
            for name, paths in collisions.items():
                print(f"     '{name}':")
                for p in paths:
                    print(f"       - {p}")
        else:
            print(f"\n  ✅ No collisions detected!")

        # Validate all names are valid directory names
        print("\n5️⃣ Directory Name Validation:")
        invalid_names = []
        for name in name_map:
            if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$", name):
                invalid_names.append(name)

        if invalid_names:
            print(f"  ❌ Invalid directory names ({len(invalid_names)}):")
            for name in invalid_names[:5]:
                print(f"     - '{name}'")
        else:
            print(f"  ✅ All {len(name_map)} names are valid directory names!")

        # Summary
        print("\n6️⃣ Summary:")
        print("-" * 60)
        total = len(all_skill_files)
        unique = len(unique_names) + len(collisions)

        print(f"  Total SKILL.md files: {total}")
        print(f"  Unique flat names: {len(unique_names)}")
        print(f"  Collisions: {len(collisions)}")
        print(f"  Missing names: {len(missing_names)}")

        is_pass = len(collisions) == 0 and len(invalid_names) == 0
        if is_pass:
            print(f"\n  ✅ ALL CHECKS PASSED")
        else:
            print(f"\n  ⚠️  SOME CHECKS NEED ATTENTION")

        print("\n✨ Analysis complete!")

        return {
            "total": total,
            "unique": len(unique_names),
            "collisions": len(collisions),
            "missing_names": len(missing_names),
            "invalid_names": len(invalid_names),
            "passed": is_pass,
        }


if __name__ == "__main__":
    try:
        results = analyze_skill_locations()

        print("\n" + "=" * 60)
        print("FINAL VERDICT")
        print("=" * 60)

        if results["passed"]:
            print("\n✅ V4 FLAT STRUCTURE IS VALID")
            print("   All names are unique and valid directory names!")
        else:
            print("\n⚠️  V4 FLAT STRUCTURE NEEDS FIXES")
            if results["collisions"] > 0:
                print(f"   {results['collisions']} name collisions to resolve")
            if results["invalid_names"] > 0:
                print(f"   {results['invalid_names']} invalid directory names")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
