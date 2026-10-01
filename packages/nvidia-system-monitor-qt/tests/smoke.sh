#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nvidia-system-monitor-qt
test -x /usr/bin/qnvsm
test -f /usr/share/applications/qnvsm.desktop
test -f /usr/share/icons/hicolor/512x512/apps/qnvsm.png
