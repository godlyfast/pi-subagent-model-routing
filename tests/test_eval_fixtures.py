"""Offline regression tests for the tabletop eval scenario input seam.

The seam under test is the documented evaluator input for a scenario: its
``prompt`` plus exactly the fixture files listed in its ``files`` array in
``evals/evals.json``, resolved inside this repository. Safety-fact checks read
only that combined context; they never read the ``assertions`` arrays or the
shared references to decide what the context must contain. Expected contract
values come from independently pinned pre-refactor baseline digests.

Standard library only, no network. Run offline with:

    python3 -m unittest discover -s tests -v
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_PATH = REPO_ROOT / "evals" / "evals.json"

BRIDGE_FIXTURE = "evals/fixtures/bridge-facts-claude-0.9.3-antigravity-1.8.4.md"
ADVISOR_FIXTURE = "evals/fixtures/advisor-facts-rpiv-advisor-2.13.9.md"
ROUTING_FIXTURE = "evals/fixtures/routing-facts-pi-subagents-0.79.2.md"

# Independent pins taken from the pre-refactor baseline evals snapshot: the
# id/name/expected_output/assertions contract, the complete records of cases
# 1-5, and the bytes of the original pi-subagents fixture.
BASELINE_CONTRACT_DIGEST = "f68c153e954de3d1f03ada09452315640bf6a894f7d04926957cac368a66ebc5"
BASELINE_CASES_1_TO_5_DIGEST = "581042811e55c2a3848e88a216794c11cd3eb1bb7509029a603ecafb85992f79"
BASELINE_ROUTING_FIXTURE_DIGEST = "d8e6afc2e27f08f009e27f8138b34bf51dda4ea79b3b3885dfe74cf92cd8dfc6"
BASELINE_IDS = [1, 2, 3, 4, 5, 6, 7, 8]
BASELINE_NAMES = [
    "audit-mode-command-gates",
    "chart-to-registry-mapping-unknown-quota",
    "override-precedence-debugging",
    "primary-429-no-fallback",
    "subscription-bridge-route-identity",
    "bridge-native-tools-child-delivery",
    "optional-advisor-recommendation-and-executor-blocklist",
    "advisor-xdg-missing-effort-and-bridge-safety",
]
BASELINE_ASSERTION_COUNTS = [4, 5, 5, 5, 5, 5, 5, 5]


def load_evals():
    return json.loads(EVALS_PATH.read_text(encoding="utf-8"))["evals"]


def scenario(eval_id):
    for entry in load_evals():
        if entry["id"] == eval_id:
            return entry
    raise AssertionError("scenario id missing: %d" % eval_id)


def _digest(records):
    payload = "\n".join(
        json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def contract_digest():
    return _digest([
        {
            "id": entry["id"],
            "name": entry["name"],
            "expected_output": entry["expected_output"],
            "assertions": entry["assertions"],
        }
        for entry in load_evals()
    ])


def cases_1_to_5_digest():
    return _digest([
        {key: entry[key] for key in ("id", "name", "prompt", "expected_output", "files", "assertions")}
        for entry in load_evals()
        if entry["id"] <= 5
    ])


def scenario_input_context(entry):
    """Combined evaluator input text at the seam: prompt plus listed fixtures."""
    parts = [entry["prompt"]]
    for rel in entry["files"]:
        parts.append((REPO_ROOT / rel).read_text(encoding="utf-8"))
    return "\n".join(parts)


class BaselineContractTests(unittest.TestCase):
    """The published eval contract must not drift from the baseline snapshot."""

    def test_ids_names_expected_outputs_assertions_match_baseline_pin(self):
        self.assertEqual([e["id"] for e in load_evals()], BASELINE_IDS)
        self.assertEqual([e["name"] for e in load_evals()], BASELINE_NAMES)
        self.assertEqual(
            [len(e["assertions"]) for e in load_evals()], BASELINE_ASSERTION_COUNTS
        )
        self.assertEqual(sum(BASELINE_ASSERTION_COUNTS), 39)
        self.assertEqual(contract_digest(), BASELINE_CONTRACT_DIGEST)

    def test_cases_1_to_5_records_unchanged_from_baseline_pin(self):
        self.assertEqual(cases_1_to_5_digest(), BASELINE_CASES_1_TO_5_DIGEST)

    def test_original_routing_fixture_bytes_unchanged(self):
        digest = hashlib.sha256(
            (REPO_ROOT / ROUTING_FIXTURE).read_bytes()
        ).hexdigest()
        self.assertEqual(digest, BASELINE_ROUTING_FIXTURE_DIGEST)

    def test_every_scenario_fixture_reference_resolves_inside_repository(self):
        for entry in load_evals():
            for rel in entry["files"]:
                with self.subTest(scenario=entry["id"], fixture=rel):
                    fixture_path = Path(rel)
                    self.assertFalse(fixture_path.is_absolute())
                    resolved = (REPO_ROOT / rel).resolve()
                    resolved.relative_to(REPO_ROOT.resolve())
                    self.assertTrue(resolved.is_file())
                    self.assertEqual(resolved.parent, (REPO_ROOT / "evals" / "fixtures"))


class Case6BridgeFixtureTests(unittest.TestCase):
    """Case 6 input seam: dated bridge fixture plus case-specific prompt facts."""

    CASE_ID = 6

    def setUp(self):
        self.case = scenario(self.CASE_ID)

    def test_case6_lists_only_the_dated_bridge_fixture(self):
        self.assertEqual(self.case["files"], [BRIDGE_FIXTURE])

    def test_case6_context_keeps_bridge_safety_facts(self):
        context = scenario_input_context(self.case)
        for fact in (
            "tools: []",
            "hooks can still run",
            "prompt projection",
            "different subagent package",
            "outside Pi's forwarded-tool allowlist",
            "read-only reviewer",
            "directory roots",
            "package-manifest",
            "active approval gate",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, context)

    def test_case6_prompt_keeps_installation_and_teammate_facts(self):
        for fact in (
            "Audit only",
            "no detected permission extension",
            "No actual child integration is tested",
            "Git worktree",
            "disabling readOnly if refused",
            "AskClaude",
            "AskAntigravity",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.case["prompt"])

    def test_bridge_fixture_is_dated_frozen_test_truth_with_version_pins(self):
        text = (REPO_ROOT / BRIDGE_FIXTURE).read_text(encoding="utf-8")
        for fact in (
            "Fixture, not live truth",
            "frozen test truth",
            "2026-10-20",
            "0.9.3",
            "1.8.4",
            "fa2d7a3d3a3f234bad86877928aeef4797680082",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, text)


class Case7AdvisorFixtureTests(unittest.TestCase):
    """Case 7 input seam: dated Advisor fixture plus case-specific prompt facts."""

    CASE_ID = 7

    def setUp(self):
        self.case = scenario(self.CASE_ID)

    def test_case7_lists_only_the_dated_advisor_fixture(self):
        self.assertEqual(self.case["files"], [ADVISOR_FIXTURE])

    def test_case7_context_keeps_advisor_safety_facts(self):
        context = scenario_input_context(self.case)
        for fact in (
            "executor blocklist",
            "minEffort",
            "does not exclude that candidate advisor model globally",
            "remains saved",
            "configuration picker",
            "tools: []",
            "native CLI",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, context)

    def test_case7_prompt_keeps_installation_saved_state_and_policy_facts(self):
        for fact in (
            "no Advisor plugin",
            "rpiv-advisor 2.13.9",
            "legacy/atlas",
            "effort max",
            "minEffort: high",
            "acme/driver at high",
            "cannot resolve legacy/atlas",
            "acme/oracle:low",
            "maximum supported effort",
            "native-CLI reviewers",
            "silently migrate",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.case["prompt"])

    def test_advisor_fixture_is_dated_frozen_truth_with_attribution_not_main_pin(self):
        text = (REPO_ROOT / ADVISOR_FIXTURE).read_text(encoding="utf-8")
        for fact in (
            "Fixture, not live truth",
            "frozen test truth",
            "2026-10-20",
            "2.13.9",
            "73a5a3b8ae75003958f45193ee3d2e570c223e55",
            "navigation aids",
            "not a 2.13.9 version pin",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, text)


class Case8BothFixturesTests(unittest.TestCase):
    """Case 8 input seam: both dated fixtures plus case-specific prompt facts."""

    CASE_ID = 8

    def setUp(self):
        self.case = scenario(self.CASE_ID)

    def test_case8_lists_the_bridge_and_advisor_fixtures(self):
        self.assertEqual(
            sorted(self.case["files"]), sorted([BRIDGE_FIXTURE, ADVISOR_FIXTURE])
        )

    def test_case8_context_keeps_advisor_and_bridge_safety_facts(self):
        context = scenario_input_context(self.case)
        for fact in (
            "read only if the primary is missing",
            "malformed primary wins",
            "no reasoning option",
            "explicit reasoning-off",
            "registered-tool inventory",
            "tools: []",
            "native CLI",
            "readOnly",
            "turns refuse",
            "outside Pi's forwarded-tool allowlist",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, context)

    def test_case8_prompt_keeps_snapshots_unttested_and_teammate_facts(self):
        for fact in (
            "Audit only",
            "no consultations",
            "malformed existing XDG advisor.json",
            "valid legacy default file",
            "independent owner repair",
            "antigravity/example",
            "no effort key",
            "No bridge compatibility test exists",
            "use the legacy selection",
            "explicit off",
            "/advisor",
            "advisor()",
        ):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.case["prompt"])


class MissingFixtureNegativeTests(unittest.TestCase):
    """A copied package missing a listed fixture must fail the existing checker
    specifically for that named fixture, and for nothing else."""

    def test_copied_package_with_missing_fixture_fails_checker_for_named_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Keep the package directory name so the checker's name rule is not
            # the finding under test.
            copy_root = Path(tmp) / REPO_ROOT.name
            shutil.copytree(
                REPO_ROOT,
                copy_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            (copy_root / ADVISOR_FIXTURE).unlink()
            proc = subprocess.run(
                [
                    sys.executable,
                    str(copy_root / "scripts" / "check_public_ready.py"),
                    str(copy_root),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            fail_lines = [line for line in proc.stdout.splitlines() if line.startswith("[FAIL]")]
            # One finding per scenario referencing the missing fixture (cases 7
            # and 8), all of them about that named fixture and nothing else.
            self.assertTrue(fail_lines)
            for line in fail_lines:
                with self.subTest(line=line):
                    self.assertIn("referenced file does not exist", line)
                    self.assertIn(ADVISOR_FIXTURE.rsplit("/", 1)[-1], line)
                    self.assertIn("eval structure", line)
            self.assertIn(
                "FAIL: %d finding(s) across 1 check group(s)" % len(fail_lines),
                proc.stdout,
            )


if __name__ == "__main__":
    unittest.main()
