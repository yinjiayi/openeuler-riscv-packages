<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-failures

This directory packages upstream `https://metacpan.org/dist/failures` version `0.004` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The stable source is the official CPAN release, verified against MetaCPAN and signed PAUSE checksums. The original Apache-2.0 grant and both generated-source notices are preserved by extracting their license bytes from pinned donor archives. No donor code is executed or installed.

The recipe retains the original three default test files and both fixture modules. It supplies Test::FailWarnings to exercise the original warning assertions. The installed smoke checks a typed exception's message and payload, then a custom derived exception's identity and string representation.
