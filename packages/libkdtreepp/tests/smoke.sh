#!/bin/bash
set -euo pipefail
test -r /usr/include/kdtree++/kdtree.hpp
test -r /usr/share/licenses/libkdtree++/COPYING
test -x /usr/share/libkdtreepp/run-tests.sh
/usr/share/libkdtreepp/run-tests.sh
