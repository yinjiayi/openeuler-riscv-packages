#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cabextract
installed_version=$(rpm -q --qf '%{VERSION}' cabextract)
cabextract --version | grep -F "cabextract version ${installed_version}"
