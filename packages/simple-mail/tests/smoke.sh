#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- simple-mail simple-mail-devel
test -e /usr/lib64/libSimpleMail3Qt5.so.0
test -e /usr/lib64/libSimpleMail3Qt5.so.3.1.0
test -e /usr/lib64/libSimpleMail3Qt5.so
test -e /usr/include/simplemail3-qt5/SimpleMail/SimpleMail
test -e /usr/lib64/cmake/SimpleMail3Qt5/SimpleMail3Qt5Config.cmake
test -e /usr/lib64/pkgconfig/SimpleMail3Qt5.pc
