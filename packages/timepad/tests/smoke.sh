#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- timepad
test -x /usr/bin/Timepad
test -f /usr/share/applications/timepad.desktop
grep -Fxq 'Exec=Timepad' /usr/share/applications/timepad.desktop
grep -Fxq 'Icon=timepad' /usr/share/applications/timepad.desktop
test -f /usr/share/icons/hicolor/256x256/apps/timepad.png
test -f '/usr/share/timepad/fonts/Roboto-Regular.ttf'
test -f '/usr/share/timepad/sound/freesound_community-kitchen-timer-87485.mp3'
if ldd /usr/bin/Timepad | grep -F 'not found'; then
  exit 1
fi
