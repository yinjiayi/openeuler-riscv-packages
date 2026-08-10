#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libexif libexif-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <libexif/exif-data.h>
int main(void) {
  ExifData *data = exif_data_new();
  if (!data) return 1;
  exif_data_unref(data);
  return 0;
}
C
gcc "$task_dir/smoke.c" -lexif -o "$task_dir/smoke"
"$task_dir/smoke"
