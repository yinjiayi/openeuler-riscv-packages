<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcuckoo

This packages official stable `v0.3.1` of `efficient/libcuckoo` for openEuler
24.03 LTS SP3 `riscv64`/RVA23. Libcuckoo is a C++11 header-only concurrent hash
table with C interface templates and CMake exports. The annotated tag resolves
to commit `ea8c36c65bf9cf83aaf6b0db971248c6ae3686cf`. Its fixed commit archive
has SHA-256 `4d1672bc26cc681662e326966d614df712c55358dc6aa605a62baba65e53908c`;
all 64 archive files were matched to official Git blobs without execution.
No detached archive signature is supplied by the reviewed release metadata;
this is HTTPS, SHA-256 and Git-object verification, not local signing-key trust.

The discovery snapshot retains Arch, Debian and openSUSE lineage; their
recipes were not executed. Fresh target primary and filelists metadata covered
18,503 official and 1,223 supplemental records. No matching package, CMake
capability or installed header path was found. Complete open-PR metadata
identity checks found no canonical duplicate. Ten dependency roots exist;
the 124-record capability closure has no missing name. Literal bounds were
reviewed separately, including the versionless libxcrypt-static alias's owning
4.4.36 package; this does not claim a verified DNF transaction or SAT solution.

The recipe retains the original default header/C-interface/CMake installation.
Upstream defaults enable no test or example builds. We additionally enable
`BUILD_UNIT_TESTS` and `BUILD_EXAMPLES`: the original one-entry CTest suite
executes the 80 declared Catch test cases without filters, while all original
example targets compile. Assertions remain enabled. Optional stress and
benchmark flags remain at upstream defaults, not disabled from an enabled
suite. QEMU unit checks do not certify native concurrency, timing or throughput;
performance and hardware validation require native RISC-V.

Installed smoke verifies RPM ownership/integrity, imports the installed exact
CMake package, then rebuilds/runs the same original unit suite and builds the
same examples using installed headers. The QA tree contains original tests
and examples but no fallback copies of the installed library headers. No
patch or upstream source edit is introduced. Apache-2.0 upstream notices,
the bundled Catch BSL-1.0 license and PCG Apache-2.0 notices remain intact.

Build and installed-smoke success remain new-head CI acceptance gates. Local
work is limited to inert source verification and trusted repository validation;
it is not an RPM/QEMU build and produces no RPM/SRPM success claim or URL.

The first exact-head target run completed all 80 original cases (203,960
assertions), then failed packaging an empty automatic debuginfo subpackage.
The installed payload has no ELF files: it consists of headers, CMake metadata
and QA source. The recipe therefore disables only the automatic debuginfo
subpackage. Original builds, examples, tests, installation and installed QA
remain unchanged; the corrected head still requires fresh full CI acceptance.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The October 17 license audit found that the original root `LICENSE` is an
Apache-2.0 grant/URL notice, not a complete copy of the license terms. A separate
official ASF source, `https://www.apache.org/licenses/LICENSE-2.0.txt`, is pinned
with SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`
and installed as `%license` beside the unchanged upstream notice and complete
Catch BSL-1.0 text. Installed QA checks both Apache text and notice digests.
All 64 original upstream files, the complete original unit/example commands,
assertions, and installed-header-only test strategy remain unchanged. This
corrects a static distribution defect even though the old head's CI was green;
it is not a fabricated CI failure or proof of replacement-head build success.
The branch includes current main's normal all-binary RPM installation workflow;
replacement-head full CI and physical RPM/SRPM/license acceptance remain required.
