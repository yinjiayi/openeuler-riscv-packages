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
oe_runner_base=$test_root/base
oe_runner_libexec=$test_root/libexec
oe_runner_config=$test_root/config
runner_name=oe-rva23-qemu-201
runner_dir=$(oe_runner_dir "$runner_name")
mkdir -p "$runner_dir"
oe_run() {
  if [[ ${1-} == systemctl ]]; then
    printf '%s\n' openeuler-actions-runner@.service "$(oe_service_name "$runner_name")"
  else
    command "$@"
  fi
}
oe_check_no_other_runners "$runner_name"
if (
  oe_run() { printf '%s\n' actions.runner.unexpected.service; }
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
