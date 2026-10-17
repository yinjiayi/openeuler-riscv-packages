<!-- SPDX-License-Identifier: Apache-2.0 -->
# libchan

This directory packages upstream `https://github.com/tylertreat/chan` version `0.0.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official tag `0.0.4` resolves to `b4120abe5d642284182f04965e793cc918daf711`.
The fixed codeload archive SHA-256 is
`82055bc8e8ecbf430edbfbaad3bdf1f55f65dec8c4f54d316b84e3879084b0a2`.
All 18 Git blobs were independently checked. Historical AUR `libchan 0.0.4-2`
is retained as stale discovery lineage, not official release authority; no AUR
recipe was executed or copied. Full upstream Apache-2.0 `LICENSE` is installed;
the fixed tree has no `NOTICE` member. No source patch is proposed.

Default Autotools shared/static features, original C99 flags and examples remain
enabled. `%check` invokes the complete original `make check`/`src/chan_test`
used by upstream Travis, including buffered/unbuffered synchronization, closing,
select, typed values and 100-thread cases. The unchanged original source is
SHA-256-bound and recompiled against staged and installed public headers and
shared/static libraries at O0/O2. The replay driver checks the actual shared
SONAME/loader path and rejects unexpected RPATH or accidental dynamic linking
in the static-libchan replay. A 300-second timeout is a failure, not a skip.
Each original executable reports 14 test groups; repeated executions are not
additional unique upstream tests. This is functional concurrency coverage, not
performance, formal thread-safety, scheduler fairness or native timing proof.

Complete configured official/supplemental primary+filelists joins found no package,
header, SONAME or library collision and no missing dependency provider. Provider
presence is not a DNF SAT/build/install proof; target CI must establish those.
Local verification is limited to trusted repository unit/golden/metadata checks,
shell syntax and checksum-only source materialization. No local upstream, RPM
or QEMU execution. Exact-head target CI and physical RPM/SRPM acceptance remain
independent gates. Auto-merge stays disabled and RISC-V status remains unknown
until authentic target evidence is accepted.
