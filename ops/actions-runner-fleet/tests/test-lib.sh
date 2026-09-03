#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
# shellcheck disable=SC1091
source "$source_dir/_lib.sh"

oe_validate_host_name 10.230.50.201 oe-rva23-qemu-201
oe_validate_host_name 10.230.50.250 oe-rva23-qemu-250
[[ $(oe_host_from_name oe-rva23-qemu-224) == 10.230.50.224 ]]
[[ $(oe_rollout_stage 10.230.50.201) == canary ]]
[[ $(oe_rollout_stage 10.230.50.206) == clean-expansion ]]
[[ $(oe_rollout_stage 10.230.50.231) == conditional ]]

if (oe_validate_host_name 10.230.50.200 oe-rva23-qemu-200) 2>/dev/null; then
  printf 'out-of-fleet host was accepted\n' >&2
  exit 1
fi
if (oe_validate_host_name 10.230.50.201 oe-rva23-qemu-202) 2>/dev/null; then
  printf 'mismatched runner name was accepted\n' >&2
  exit 1
fi
if (oe_reject_secret_arguments --token hidden) 2>/dev/null; then
  printf 'credential argument was accepted\n' >&2
  exit 1
fi

oe_load_release_lock "$source_dir/runner-release.lock"
[[ $RUNNER_VERSION == 2.336.0 ]]
[[ $RUNNER_SIZE == 226035903 ]]
oe_load_cleanup_image_lock "$source_dir/cleanup-image.lock"
[[ $CLEANUP_IMAGE_REF =~ @sha256:[0-9a-f]{64}$ ]]

test_root=$(mktemp -d)
trap 'rm -rf -- "$test_root"' EXIT

fake_systemctl=$test_root/systemctl
printf '#!/bin/sh\nexit 0\n' >"$fake_systemctl"
chmod 0755 "$fake_systemctl"
integrity_probe() (
  local mismatch=${1:?}
  oe_systemctl_path=$fake_systemctl
  stat() {
    printf '%s\n' root:root:755
  }
  dpkg-query() {
    case ${1-} in
      --search)
        printf '%s\n' 'systemd: /usr/bin/systemctl'
        ;;
      --show)
        printf 'systemd\tinstall ok installed\t259.5-0ubuntu3.4\n'
        ;;
      --verify)
        if [[ $mismatch == true ]]; then
          printf '%s\n' '??5??????   /usr/bin/systemctl'
        fi
        return 0
        ;;
      *)
        return 2
        ;;
    esac
  }
  oe_assert_systemctl_integrity
)
integrity_probe false
if integrity_probe true 2>/dev/null; then
  printf 'systemd verification output with rc=0 was accepted\n' >&2
  exit 1
fi

systemctl_marker=$test_root/systemctl-called
if (
  oe_assert_systemctl_integrity() { oe_die 'simulated package-integrity failure'; }
  oe_systemctl() { : >"$systemctl_marker"; }
  oe_assert_platform false
) 2>/dev/null; then
  printf 'platform check accepted failed systemctl integrity\n' >&2
  exit 1
fi
[[ ! -e $systemctl_marker ]] || {
  printf 'systemctl ran before package integrity passed\n' >&2
  exit 1
}

oe_runner_base=$test_root/base
oe_runner_lock_dir=$oe_runner_base/.locks
oe_runner_config=$test_root/config
runner_name=oe-rva23-qemu-201
runner_dir=$(oe_runner_dir "$runner_name")
mkdir -p "$runner_dir" "$oe_runner_lock_dir"
repository_name=${oe_runner_repo_slug#*/}
work_dir=$runner_dir/_work
job_workspace=$work_dir/$repository_name/$repository_name
mkdir -p "$job_workspace" "$work_dir/_actions/pinned-action"
[[ $(oe_job_workspace "$work_dir" "$job_workspace") == "$job_workspace" ]]
if (oe_job_workspace "$work_dir" "$work_dir/_actions/pinned-action") 2>/dev/null; then
  printf 'Runner action cache was accepted as a job workspace\n' >&2
  exit 1
fi
oe_systemctl() {
  printf '%s\n' openeuler-actions-runner@.service "$(oe_service_name "$runner_name")"
}
oe_check_no_other_runners "$runner_name"
if (
  oe_systemctl() { printf '%s\n' actions.runner.unexpected.service; }
  oe_check_no_other_runners "$runner_name"
) 2>/dev/null; then
  printf 'another runner service was accepted\n' >&2
  exit 1
fi
mkdir "$oe_runner_base/unmanaged-runner"
if (oe_check_no_other_runners "$runner_name") 2>/dev/null; then
  printf 'another runner directory was accepted\n' >&2
  exit 1
fi

printf 'runner fleet shell guards passed\n'
