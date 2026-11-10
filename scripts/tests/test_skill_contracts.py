# SPDX-License-Identifier: Apache-2.0
"""Validate documented CLI contracts without building, fetching, or mutating GitHub.

These tests exercise the real argument parsers, not snapshots of instruction
wording. Behavioral orchestration review remains separate from syntax checks.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import pathlib
import re
import shlex
import sys
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
SKILLS = ROOT / "skills"
sys.path.insert(0, str(SCRIPTS))

VALUES = {
    "candidate_limit": "0",
    "aur_stale_days": "730",
    "update_shard_size": "100",
    "shard_index": "0",
    "requests_per_second": "2",
    "retry_count": "3",
    "pr_number": "123",
    "github_repo": "yinjiayi/openeuler-riscv-packages",
    "failed_head_sha": "a" * 40,
    "pushed_head_sha": "b" * 40,
    "main_sha": "c" * 40,
    "as_of": "2026-11-06T00:00:00Z",
    "generated_at": "2026-11-06T00:00:00Z",
    "package_id": "example-package",
    "worker_id": "worker-a",
    "repair_owner": "worker-a",
}


def substitute(token):
    def replacement(match):
        name = match.group(1) or match.group(3)
        return VALUES.get(name, match.group(2) or "fixture/" + name)
    return re.sub(r"\$\{([A-Za-z_][A-Za-z_0-9]*)(?::-([^}]+))?\}|\$([A-Za-z_][A-Za-z_0-9]*)", replacement, token)


def examples():
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        blocks = re.findall(r"```(?:bash|sh)\n(.*?)```", skill.read_text(), re.S)
        for block in blocks:
            for line in block.replace("\\\n", " ").splitlines():
                argv = shlex.split(line, comments=True)
                if argv and argv[0] in {"python3", "python"}:
                    argv = argv[1:]
                if argv and re.fullmatch(r"(?:\./)?scripts/[a-z0-9-]+", argv[0]):
                    yield skill.parent.name, pathlib.Path(argv[0]).name, [substitute(value) for value in argv[1:]]


def parse_example(name, arguments):
    if name == "evaluate-golden":
        name, arguments = "golden-eval", ["evaluate", *arguments]
    path = SCRIPTS / name
    if not path.is_file():
        raise AssertionError("Documented executable is absent: %s" % path)
    module_name = "skill_contract_" + name.replace("-", "_")
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    with mock.patch("subprocess.run", side_effect=AssertionError("CLI parsing must not run commands")), mock.patch(
        "subprocess.Popen", side_effect=AssertionError("CLI parsing must not start processes")
    ):
        loader.exec_module(module)
        factory = getattr(module, "parser", None) or getattr(module, "build_parser", None)
        if factory is None:
            raise AssertionError("No parser factory for documented command %s" % name)
        return factory().parse_args(arguments)


class SkillContracts(unittest.TestCase):
    def test_repository_discovery_uses_canonical_skills(self):
        discovery = ROOT / ".agents" / "skills"
        canonical = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual({path.name for path in discovery.iterdir()}, canonical)
        for name in canonical:
            with self.subTest(skill=name):
                link = discovery / name
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), (SKILLS / name).resolve())

    def test_examples_match_real_command_interfaces(self):
        commands = list(examples())
        self.assertGreater(len(commands), 10, "No substantive command examples were checked")
        for skill, tool, argv in commands:
            with self.subTest(skill=skill, tool=tool, argv=argv):
                parse_example(tool, argv)

    def test_local_build_examples_only_verify_sources(self):
        builds = [(skill, argv) for skill, tool, argv in examples() if tool == "build-rpm"]
        self.assertTrue(builds)
        for skill, argv in builds:
            with self.subTest(skill=skill):
                args = parse_example("build-rpm", argv)
                self.assertTrue(args.verify_only)
                self.assertFalse(args.skip_install_smoke)

    def test_repair_examples_keep_live_exact_head_authorization(self):
        claims = [(skill, argv) for skill, tool, argv in examples() if tool == "claim-repair"]
        self.assertTrue(claims)
        for skill, argv in claims:
            with self.subTest(skill=skill, argv=argv):
                args = parse_example("claim-repair", argv)
                self.assertEqual(args.expected_head_sha, VALUES["failed_head_sha"])
                self.assertIsNone(args.fixture_pr)
                self.assertEqual(args.repo, VALUES["github_repo"])
                if args.command == "claim":
                    self.assertTrue(args.queue)
                if args.command == "release":
                    self.assertEqual(args.pushed_head_sha, VALUES["pushed_head_sha"])

    def test_ui_metadata_binds_invocation_to_its_skill(self):
        for skill in sorted(SKILLS.glob("*/SKILL.md")):
            with self.subTest(skill=skill.parent.name):
                # Interface values use the documented quoted-string YAML subset;
                # JSON decoding also rejects broken escaping or unterminated text.
                metadata = skill.parent / "agents" / "openai.yaml"
                values = {}
                for line in metadata.read_text().splitlines():
                    match = re.fullmatch(r"  (display_name|short_description|default_prompt): (.+)", line)
                    if match:
                        values[match.group(1)] = json.loads(match.group(2))
                self.assertEqual(set(values), {"display_name", "short_description", "default_prompt"})
                self.assertIn("$" + skill.parent.name, values["default_prompt"])
                self.assertTrue(25 <= len(values["short_description"]) <= 64)


if __name__ == "__main__":
    unittest.main()
