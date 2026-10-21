#!/bin/bash
set -euo pipefail
test -s /usr/include/dlibxx.hxx
test -s /usr/lib64/libdlibxx.so.1.0.0
test -L /usr/lib64/libdlibxx.so
test -s /usr/share/licenses/libdlibxx/LICENSE
test -s /usr/share/doc/libdlibxx/README.md
exec /usr/share/libdlibxx/run-tests.sh /usr/share/libdlibxx /usr/include /usr/lib64
