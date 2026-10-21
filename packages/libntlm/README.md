<!-- SPDX-License-Identifier: Apache-2.0 -->
# libntlm

This directory packages upstream libntlm 1.8 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. The official Savannah archive is pinned by SHA-256 in
sources.yaml; the frozen distribution records are discovery lineage only.

The source combines LGPL-2.1-or-later library code with GPL-3.0-or-later
gnulib components. The upstream make check suite, including its
CVE-2019-17455 regression test, remains enabled. Target Package CI may fetch
the verified source and dependencies online; no target build was performed
locally.
