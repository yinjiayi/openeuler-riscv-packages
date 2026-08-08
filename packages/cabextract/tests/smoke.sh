#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cabextract
cabextract --version | grep -F 'cabextract version 1.11'
