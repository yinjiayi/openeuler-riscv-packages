#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

case $# in
  0)
    rpm_location=()
    ;;
  1)
    [[ $1 == /rootfs ]] || {
      printf 'rpm-manifest: the optional root must be exactly /rootfs\n' >&2
      exit 2
    }
    rpm_location=(--root "$1")
    ;;
  2)
    [[ $1 == --dbpath && $2 =~ ^/[A-Za-z0-9._/-]+$ \
       && $2 != / && $2 != *//* ]] || {
      printf 'rpm-manifest: --dbpath requires a canonical absolute path\n' >&2
      exit 2
    }
    IFS=/ read -r -a dbpath_components <<<"$2"
    for component in "${dbpath_components[@]}"; do
      [[ $component != . && $component != .. ]] || {
        printf 'rpm-manifest: --dbpath contains a traversal component\n' >&2
        exit 2
      }
    done
    rpm_location=(--dbpath "$2")
    ;;
  *)
    printf 'usage: rpm-manifest.sh [/rootfs | --dbpath ABSOLUTE_PATH]\n' >&2
    exit 2
    ;;
esac

rpm "${rpm_location[@]}" -qa \
  --qf '%{NAME}\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\t%{ARCH}\t%{SHA1HEADER}\t%{SHA256HEADER}\n' \
  | LC_ALL=C sort \
  | LC_ALL=C awk -F '\t' '
      NF != 5 || $1 == "" || $2 == "" || $3 == "" ||
      length($4) != 40 || $4 !~ /^[0-9a-f]+$/ ||
      length($5) != 64 || $5 !~ /^[0-9a-f]+$/ {
        printf "rpm-manifest: invalid identity or header digest at record %d\n", NR > "/dev/stderr"
        exit 1
      }
      { print }
    '
