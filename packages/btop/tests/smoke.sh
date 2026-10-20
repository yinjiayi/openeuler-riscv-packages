#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- btop
test -x /usr/bin/btop
btop --version | grep -F '1.4.7'
btop --help >/dev/null
btop --default-config >/dev/null
test -d /usr/share/btop/themes
test -s /usr/share/applications/btop.desktop
test -s /usr/share/icons/hicolor/48x48/apps/btop.png
test -s /usr/share/icons/hicolor/scalable/apps/btop.svg
