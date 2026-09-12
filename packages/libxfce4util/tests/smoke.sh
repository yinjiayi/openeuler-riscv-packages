#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxfce4util
xfce4-kiosk-query -v
rpm -q --whatprovides 'pkgconfig(libxfce4util-1.0)'
