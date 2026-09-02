#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

case $# in
  0)
    rpm_root=()
    ;;
  1)
    [[ $1 == /rootfs ]] || {
      printf 'rpm-manifest: the optional root must be exactly /rootfs\n' >&2
      exit 2
    }
    rpm_root=(--root "$1")
    ;;
  *)
    printf 'usage: rpm-manifest.sh [/rootfs]\n' >&2
    exit 2
    ;;
esac

rpm "${rpm_root[@]}" -qa \
  --qf '%{NAME}\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\t%{ARCH}\t%{SIGPGP:pgpsig}\n' \
  | LC_ALL=C sort
