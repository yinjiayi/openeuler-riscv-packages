# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import os
import pathlib
import subprocess
from typing import Any, Mapping, Sequence


SCRIPTS = pathlib.Path(__file__).resolve().parents[1]


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_tool(name: str, arguments: Sequence[str], cwd: pathlib.Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [str(SCRIPTS / name)] + list(arguments),
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != expected:
        raise AssertionError(
            "%s returned %s, expected %s\nstdout:\n%s\nstderr:\n%s"
            % (name, completed.returncode, expected, completed.stdout, completed.stderr)
        )
    return completed
