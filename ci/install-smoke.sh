#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

package_dir=${1:-}
work_dir=${2:-}
result_file=${3:-artifacts/smoke-result.json}
repository_evidence=${4:-}
package_id=$(basename "$package_dir")
started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
status=failed
message=
dnf_transaction_file=$(dirname "$result_file")/dnf-transaction.json

write_result() {
  RESULT_STATUS=$status RESULT_MESSAGE=$message RESULT_PACKAGE=$package_id \
  RESULT_STARTED=$started_at python3 - "$result_file" <<'PY'
import datetime
import json
import os
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
payload = {
    "schema_version": 1,
    "package_id": os.environ["RESULT_PACKAGE"],
    "phase": "rpm-install-smoke",
    "status": os.environ["RESULT_STATUS"],
    "message": os.environ["RESULT_MESSAGE"],
    "started_at": os.environ["RESULT_STARTED"],
    "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}
trap write_result EXIT

[[ $package_id =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { message="invalid package id"; exit 2; }
[[ -d $package_dir && -d $work_dir ]] || { message="package or work directory is missing"; exit 2; }

if python3 - "$package_dir/package.yaml" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as handle:
    package = json.load(handle)
raise SystemExit(0 if package.get("build", {}).get("profile") == "needs-native-riscv" else 1)
PY
then
  status=needs-native-riscv
  message="package policy requires native RISC-V validation; no self-hosted runner is configured"
  exit 1
fi

rpm_root="$work_dir/RPMS"
[[ -d $rpm_root ]] || { message="binary RPM output directory is missing"; exit 1; }
mapfile -d '' rpms < <(find "$rpm_root" -type f -name '*.rpm' \
  ! -name '*-debuginfo-*' ! -name '*-debugsource-*' -print0 | sort -z)
((${#rpms[@]} > 0)) || { message="no binary RPM was produced"; exit 1; }

supplemental_repo=/etc/yum.repos.d/openeuler-riscv-project.repo
[[ -f $supplemental_repo && ! -L $supplemental_repo ]] || {
  message="verified supplemental repository configuration is missing"
  exit 1
}
[[ -f $repository_evidence && ! -L $repository_evidence ]] || {
  message="supplemental repository resolution evidence is missing"
  exit 1
}

repository_status=$(python3 - "$supplemental_repo" "$repository_evidence" <<'PY'
import configparser
import json
import re
import sys

repository_path, evidence_path = sys.argv[1:]
with open(evidence_path, encoding="utf-8") as handle:
    evidence = json.load(handle)
parser = configparser.ConfigParser(interpolation=None, strict=True)
with open(repository_path, encoding="utf-8") as handle:
    parser.read_file(handle)
if parser.sections() != ["openeuler-riscv-project"]:
    raise SystemExit("supplemental repository file has unexpected sections")
repository = parser["openeuler-riscv-project"]
expected_keys = {
    "name", "baseurl", "enabled", "gpgcheck", "repo_gpgcheck",
    "metadata_expire", "skip_if_unavailable", "module_hotfixes",
}
if (
    evidence.get("kind") != "supplemental-repository-resolution"
    or evidence.get("state_url") != "http://2.27.148.101:38080/state.json"
    or set(repository) != expected_keys
    or repository.get("gpgcheck") != "0"
    or repository.get("repo_gpgcheck") != "0"
    or repository.get("metadata_expire") != "never"
    or repository.get("module_hotfixes") != "1"
):
    raise SystemExit("supplemental repository evidence or trust policy is invalid")
status = evidence.get("status", "passed")
if status == "passed":
    generation = str(evidence.get("generation", ""))
    state_sha = str(evidence.get("state_sha256", ""))
    binary = evidence.get("repositories", {}).get("riscv64", {})
    if (
        not re.fullmatch(r"(?:bootstrap-[0-9]{8}T[0-9]{6}Z|[a-z0-9-]+-[0-9a-f]{40}-[1-9][0-9]*-[1-9][0-9]*)", generation)
        or not re.fullmatch(r"[0-9a-f]{64}", state_sha)
        or repository.get("baseurl") != binary.get("baseurl")
        or repository.get("enabled") != "1"
        or repository.get("skip_if_unavailable") != "0"
    ):
        raise SystemExit("verified supplemental repository configuration is invalid")
elif status == "unavailable":
    if (
        evidence.get("reason") != "endpoint-unavailable"
        or evidence.get("generation") is not None
        or evidence.get("state_sha256") is not None
        or evidence.get("repositories") != {}
        or evidence.get("fallback") != {
            "active_repository_ids": ["openeuler-rva23"],
            "supplemental_repository_enabled": False,
        }
        or repository.get("baseurl") != "http://2.27.148.101:38080/"
        or repository.get("enabled") != "0"
        or repository.get("skip_if_unavailable") != "1"
    ):
        raise SystemExit("official-repository-only fallback is invalid")
else:
    raise SystemExit("supplemental repository status is invalid")
print(status)
PY
)

enabled_repositories=(--enablerepo=openeuler-rva23)
if [[ $repository_status = passed ]]; then
  enabled_repositories+=(--enablerepo=openeuler-riscv-project)
fi
set +e
python3 ci/run-dnf-transaction \
  --evidence "$dnf_transaction_file" \
  --budget-seconds 3300 \
  --attempt-timeouts-seconds 2100,1100 \
  --retry-delay-seconds 5 \
  --kill-after-seconds 10 \
  -- dnf -y --setopt=install_weak_deps=False --disablerepo='*' \
    "${enabled_repositories[@]}" install -- "${rpms[@]}"
dnf_status=$?
set -e
if ((dnf_status != 0)); then
  message="bounded RPM installation DNF transaction failed; see dnf-transaction.json"
  exit "$dnf_status"
fi

smoke="$package_dir/tests/smoke.sh"
[[ -f $smoke ]] || { message="tests/smoke.sh is missing"; exit 2; }
/bin/bash "$smoke"
status=passed
message="RPM installation and package smoke test passed"
