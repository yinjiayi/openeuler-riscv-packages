<!-- SPDX-License-Identifier: Apache-2.0 -->
# tally

This directory packages upstream `https://github.com/tenseleyFlow/tally` version `0.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `2` runs upstream's real `make test` target rather than the nonexistent
`make check` target. The test target retains its unit, golden GNU `wc` parity,
differential fuzz, and SIMD engagement checks. Its GNU coreutils 9.11 oracle is
downloaded by the upstream harness during `%check`, verified against the SHA-256
embedded in that harness, and built with fixed-repository tool and sanitizer
dependencies declared by the SPEC.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
