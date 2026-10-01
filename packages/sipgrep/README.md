<!-- SPDX-License-Identifier: Apache-2.0 -->
# sipgrep

This directory packages upstream `https://github.com/sipcapture/sipgrep` version `2.2.0` release `2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned release archive contains a stale pre-generated `configure` script that still probes PCRE1, while its `configure.ac` and source use PCRE2. The RPM preparation phase therefore regenerates `configure` and declares `libpcap-devel` and `pcre2-devel` from the fixed repository, preserving packet capture, PCRE2 matching, and the existing test phase.

Release `4` adds the standard `<arpa/inet.h>` declaration required by
the HEP transport's existing `inet_pton` calls. This preserves HEP behavior
while making the source valid with the target compiler's implicit-function
declaration policy. Its patch hunk uses explicit, nonblank unified-diff
context so the target GNU patch implementation can apply it with zero fuzz.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
