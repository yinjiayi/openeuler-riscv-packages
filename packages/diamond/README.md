<!-- SPDX-License-Identifier: Apache-2.0 -->
# diamond

This directory packages upstream `https://github.com/bbuchfink/diamond` version `2.2.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Two exact-head QEMU runs completed dependency preparation in 8-13 minutes but
were cancelled at the former 120-minute job boundary before producing an
rpmbuild result. This package therefore uses the repository's bounded
180-minute build allowance. Compiler options, features, and tests are unchanged.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 5 preserves global-ranking support and the complete 39-test
upstream suite. It supplies a per-query serial nested-task pool only when the
ordinary alignment pool is absent during global-ranking post-processing. This
prevents the null `ThreadPool` dereference observed by exact-head Package CI
without disabling global ranking, changing test selection, or sharing nested
task state between concurrent query workers.
