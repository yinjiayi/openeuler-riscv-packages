<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-io-interactive-tiny

This directory packages upstream `https://metacpan.org/dist/IO-Interactive-Tiny` version `0.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The original default suite is retained. Test::Pod and Test::Pod::Coverage exercise the documentation. The developer-only Perl::Critic file retains its original opt-in. A second execution of the original interactive test under a pseudo-terminal covers the terminal assertions that the default non-interactive harness skips. The installed smoke test verifies non-interactive behavior with input from `/dev/null`.

The sole patch adds the original Damian Conway copyright, grant, and disclaimer from IO::Interactive 0.0.6 for the derived function and test. The original code, tests, and README are unchanged. Reassess the notice patch when upstream includes the notice or removes the derived material.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
