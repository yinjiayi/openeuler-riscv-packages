#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

package_dir=${1:-}
work_dir=${2:-}
result_file=${3:-artifacts/smoke-result.json}
package_id=$(basename "$package_dir")
started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
status=failed
message=

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

dnf -y --setopt install_weak_deps=False --disablerepo='*' \
  --enablerepo=openeuler-rva23 --enablerepo=openeuler-riscv-project \
  install "${rpms[@]}"

smoke="$package_dir/tests/smoke.sh"
[[ -f $smoke ]] || { message="tests/smoke.sh is missing"; exit 2; }
/bin/bash "$smoke"
status=passed
message="RPM installation and package smoke test passed"
