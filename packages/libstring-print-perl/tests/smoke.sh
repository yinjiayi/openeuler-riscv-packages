#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Print
rpm -q --whatprovides 'perl(String::Print)'
perl -MString::Print=sprinti,sprintp -e '
  die "unexpected version\n" unless $String::Print::VERSION eq "1.02";
  die "named interpolation mismatch\n"
    unless sprinti("Hello {name}", name => "RISC-V") eq "Hello RISC-V";
  die "positional formatting mismatch\n"
    unless sprintp("Node %s", "riscv64") eq "Node riscv64";
'
