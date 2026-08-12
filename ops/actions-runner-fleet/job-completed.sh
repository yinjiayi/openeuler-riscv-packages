#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

libexec=/usr/local/libexec/openeuler-actions-runner
# shellcheck source=_lib.sh
source "$libexec/_lib.sh"
oe_load_identity
timeout --signal=KILL 5m "$libexec/cleanup.sh" --name "$OE_IDENTITY_NAME" --phase after
