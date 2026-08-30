<!-- SPDX-License-Identifier: Apache-2.0 -->
# sipgrep

This directory packages upstream `https://github.com/sipcapture/sipgrep` version `2.2.0` release `2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned release archive contains a stale pre-generated `configure` script that still probes PCRE1, while its `configure.ac` and source use PCRE2. The RPM preparation phase therefore regenerates `configure` and declares `libpcap-devel` and `pcre2-devel` from the fixed repository, preserving packet capture, PCRE2 matching, and the existing test phase.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
