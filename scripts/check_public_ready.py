#!/usr/bin/env python3
"""Offline public-readiness check for the pi-subagent-model-routing package.

Standard library only. No network, no inference, no dependency installs.

Checks:
  1. frontmatter      - SKILL.md name/description/license rules
  2. package files    - package.json pi.skills manifest, LICENSE, README presence
  3. links            - relative markdown links resolve inside the repository
  4. privacy leakage  - machine-specific paths, private identifiers, internal
                        policy markers, session-history claims
  5. eval structure   - evals/evals.json shape and referenced fixture files

Usage:
  python3 scripts/check_public_ready.py [target-dir]

Default target is the repository root that contains this script. Exit status 0
means every check passed; 1 means at least one finding was reported.
"""

import json
import re
import sys
from pathlib import Path

# Privacy findings: (compiled pattern, label). The checker's own file is exempt
# so the denylist literals are not self-matching.
PRIVACY_PATTERNS = [
    (re.compile(r"/(?:Users|home)/"), "absolute host path"),
    (re.compile(r"\$HOME\b"), "machine-specific env path"),
    (re.compile(r"\b(?:10|192\.168)\.\d{1,3}\.\d{1,3}(?:\.\d{1,3})?\b"), "private network address"),
    (re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"), "private key marker"),
    (re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"), "credential marker"),
    (re.compile(r"viking://(?:user|resources)/"), "private memory reference"),
]

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt"}

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "package.json",
    "references/operations.md",
    "evals/evals.json",
    "evals/README.md",
]


def parse_frontmatter(text):
    """Return (frontmatter dict, body) or (None, text) when no valid block opens the file."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    body = text[end + 5:]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None, text
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def iter_text_files(root, self_path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or path == self_path:
            continue
        yield path


class Findings:
    def __init__(self):
        self.items = []

    def error(self, check, where, message):
        self.items.append((check, where, message))

    @property
    def count(self):
        return len(self.items)


def check_frontmatter(root, findings):
    skill = root / "SKILL.md"
    if not skill.is_file():
        findings.error("frontmatter", "SKILL.md", "missing skill file")
        return None
    frontmatter, _ = parse_frontmatter(skill.read_text(encoding="utf-8"))
    if frontmatter is None:
        findings.error("frontmatter", "SKILL.md", "no parseable frontmatter block")
        return None
    for key in ("name", "description", "license"):
        if not frontmatter.get(key):
            findings.error("frontmatter", "SKILL.md", f"missing required key: {key}")
    name = frontmatter.get("name", "")
    if name and not NAME_RE.match(name):
        findings.error("frontmatter", "SKILL.md", f"name breaks Agent Skills naming rules: {name!r}")
    if name and name != root.name:
        findings.error("frontmatter", "SKILL.md", f"name {name!r} differs from directory name {root.name!r}")
    description = frontmatter.get("description", "")
    if len(description) > 1024:
        findings.error("frontmatter", "SKILL.md", f"description exceeds 1024 chars ({len(description)})")
    if frontmatter.get("license") not in (None, "MIT"):
        findings.error("frontmatter", "SKILL.md", f"license is {frontmatter.get('license')!r}, expected MIT")
    return frontmatter


def check_package_files(root, findings):
    manifest = root / "package.json"
    if not manifest.is_file():
        findings.error("package files", "package.json", "missing package manifest")
    else:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except ValueError as exc:
            findings.error("package files", "package.json", f"invalid JSON: {exc}")
            data = None
        if isinstance(data, dict):
            for key in ("name", "version", "license"):
                if not data.get(key):
                    findings.error("package files", "package.json", f"missing key: {key}")
            if data.get("license") not in (None, "MIT"):
                findings.error("package files", "package.json", f"license is {data.get('license')!r}, expected MIT")
            pi_skills = (data.get("pi") or {}).get("skills")
            if not isinstance(pi_skills, list) or not pi_skills:
                findings.error("package files", "package.json", "pi.skills must be a non-empty list")
            else:
                for entry in pi_skills:
                    if not isinstance(entry, str):
                        findings.error("package files", "package.json", f"pi.skills entry is not a string: {entry!r}")
                        continue
                    target = (root / entry).resolve()
                    if not target.is_file():
                        findings.error("package files", "package.json", f"pi.skills entry does not exist: {entry}")
                    elif target.suffix != ".md":
                        findings.error("package files", "package.json", f"pi.skills entry is not a markdown file: {entry}")
                    try:
                        target.relative_to(root.resolve())
                    except ValueError:
                        findings.error("package files", "package.json", f"pi.skills entry leaves the repository: {entry}")
    license_file = root / "LICENSE"
    if not license_file.is_file():
        findings.error("package files", "LICENSE", "missing LICENSE")
    else:
        text = license_file.read_text(encoding="utf-8")
        if "MIT" not in text:
            findings.error("package files", "LICENSE", "does not identify the MIT license")
        if "godlyfast" not in text:
            findings.error("package files", "LICENSE", "missing godlyfast copyright holder")
    if not (root / "README.md").is_file():
        findings.error("package files", "README.md", "missing README")


def check_links(root, findings):
    for path in iter_text_files(root, None):
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(2)
            if target.startswith("#") or SCHEME_RE.match(target):
                continue
            rel = target.split("#", 1)[0]
            if not rel:
                continue
            resolved = (path.parent / rel).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                findings.error("links", str(path.relative_to(root)), f"relative link leaves the repository: {target}")
                continue
            if not resolved.exists():
                findings.error("links", str(path.relative_to(root)), f"link target does not exist: {target}")


def check_privacy(root, findings, self_path):
    for path in iter_text_files(root, self_path):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, label in PRIVACY_PATTERNS:
                if pattern.search(line):
                    findings.error("privacy", f"{path.relative_to(root)}:{lineno}", label)


def check_evals(root, findings, frontmatter):
    evals_file = root / "evals" / "evals.json"
    if not evals_file.is_file():
        findings.error("eval structure", "evals/evals.json", "missing evals file")
        return
    try:
        data = json.loads(evals_file.read_text(encoding="utf-8"))
    except ValueError as exc:
        findings.error("eval structure", "evals/evals.json", f"invalid JSON: {exc}")
        return
    if frontmatter and data.get("skill_name") != frontmatter.get("name"):
        findings.error("eval structure", "evals/evals.json", "skill_name does not match SKILL.md name")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        findings.error("eval structure", "evals/evals.json", "evals must be a non-empty list")
        return
    seen_ids = set()
    for index, entry in enumerate(evals):
        where = f"evals/evals.json eval[{index}]"
        if not isinstance(entry, dict):
            findings.error("eval structure", where, "eval entry is not an object")
            continue
        eval_id = entry.get("id")
        if not isinstance(eval_id, int):
            findings.error("eval structure", where, "id must be an integer")
        elif eval_id in seen_ids:
            findings.error("eval structure", where, f"duplicate id {eval_id}")
        else:
            seen_ids.add(eval_id)
        for key in ("name", "prompt", "expected_output"):
            if not isinstance(entry.get(key), str) or not entry.get(key).strip():
                findings.error("eval structure", where, f"{key} must be a non-empty string")
        files = entry.get("files")
        if not isinstance(files, list):
            findings.error("eval structure", where, "files must be a list")
        else:
            for rel in files:
                if not isinstance(rel, str) or not (root / rel).is_file():
                    findings.error("eval structure", where, f"referenced file does not exist: {rel!r}")
        assertions = entry.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            findings.error("eval structure", where, "assertions must be a non-empty list")
        else:
            for assertion in assertions:
                if not isinstance(assertion, str) or not assertion.strip():
                    findings.error("eval structure", where, "empty assertion entry")
    if not (root / "evals" / "README.md").is_file():
        findings.error("eval structure", "evals/README.md", "missing eval notes")


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    self_path = Path(__file__).resolve()
    findings = Findings()
    if not root.is_dir():
        print(f"[FAIL] target is not a directory: {root}")
        return 1

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            findings.error("package files", rel, "required file missing")

    frontmatter = check_frontmatter(root, findings)
    check_package_files(root, findings)
    check_links(root, findings)
    check_privacy(root, findings, self_path)
    check_evals(root, findings, frontmatter)

    print(f"public-readiness check: {root}")
    if findings.count == 0:
        print("PASS: frontmatter, package files/links, privacy leakage, eval structure all clean")
        return 0
    by_check = {}
    for check, where, message in findings.items:
        by_check.setdefault(check, []).append(f"{where}: {message}")
    for check in ("frontmatter", "package files", "links", "privacy", "eval structure"):
        for line in by_check.get(check, []):
            print(f"[FAIL] {check} - {line}")
    print(f"FAIL: {findings.count} finding(s) across {len(by_check)} check group(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
