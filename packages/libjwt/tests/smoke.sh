#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

token=$(jwt-generate --quiet --algorithm none --no-iat)
test "$token" = "eyJhbGciOiJub25lIn0.e30."
jwt-verify --quiet --algorithm none "$token"
