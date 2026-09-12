#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gflags gflags-devel
test -x /usr/bin/gflags_completions.sh
test -e /usr/lib64/libgflags_nothreads.so

task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cc" <<'CPP'
#include <gflags/gflags.h>

DEFINE_string(target_arch, "unset", "Target architecture");

int main(int argc, char **argv) {
  gflags::ParseCommandLineFlags(&argc, &argv, true);
  return FLAGS_target_arch == "riscv64" ? 0 : 1;
}
CPP

read -r -a cxx_flags <<<"${CXXFLAGS:-}"
read -r -a gflags_flags <<<"$(pkg-config --cflags --libs gflags)"
"${CXX:-c++}" "${cxx_flags[@]}" -std=c++11 "$task_dir/smoke.cc" \
  "${gflags_flags[@]}" -o "$task_dir/smoke"
"$task_dir/smoke" --target_arch=riscv64
