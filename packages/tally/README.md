<!-- SPDX-License-Identifier: Apache-2.0 -->
# tally

This directory packages upstream `https://github.com/tenseleyFlow/tally` version `0.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `2` runs upstream's real `make test` target rather than the nonexistent
`make check` target. The test target retains its unit, golden GNU `wc` parity,
differential fuzz, and SIMD engagement checks. Its GNU coreutils 9.11 oracle is
downloaded by the upstream harness during `%check`, verified against the SHA-256
embedded in that harness, and built with fixed-repository tool and sanitizer
dependencies declared by the SPEC.

Exact-head CI run `33530707443` installed the complete dependency closure and
then reached the package's former 60-minute job boundary while the target build
was still running. The artifact contained no compiler, test, or packaging first
error, so the package metadata now grants the complete upstream test target up
to 180 minutes under QEMU without changing compiler flags or disabling tests.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
