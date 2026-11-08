<!-- SPDX-License-Identifier: Apache-2.0 -->
# scdoc

Official Scdoc 1.11.5 for openEuler 24.03 LTS SP3 riscv64/RVA23.
Fixed official source: https://git.sr.ht/~sircmpwn/scdoc/archive/1.11.5.tar.gz
SHA-256: `98780bbdf16c1bce89ef3a8c0f537ac6e4ea77087b609e7698857614488a2a62`.
All 32 release files, full source, MIT grant and nine original test drivers
were read. The original default build, compiler warnings, assertions, test
files and unfiltered `make check` remain unchanged; no source patch is added.

Upstream's test helper prints FAIL without propagating it as a failure exit.
The recipe additionally requires all nine drivers, all 56 OK results and no
FAIL results after the original default suite. Offline staged and installed
replay extract the exact original source and invoke `make -o scdoc check`
with only `./scdoc` pointing to the packaged executable. Marking that binary
old prevents rebuilding a substitute; no original test is filtered or edited.
The tests RPM includes the original source archive and its MIT license.

No local upstream code, compiler, RPM or QEMU build was executed. Real build,
default tests, install and physical RPM/SRPM acceptance require exact-head CI.
This is functional markup/formatting coverage, not native timing, security,
complete malformed-input safety or forensic attestation.
