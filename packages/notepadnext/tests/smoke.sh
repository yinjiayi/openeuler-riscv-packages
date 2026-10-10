#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- notepadnext
test "$(QT_QPA_PLATFORM=offscreen timeout 30 NotepadNext --version)" = "NotepadNext 0.14"
