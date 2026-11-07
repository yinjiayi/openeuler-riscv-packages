<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcircle

This directory packages upstream `https://github.com/hpc/libcircle` version `0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source, license and target contract

Official `hpc/libcircle` tag `v0.3` resolves to commit
`3d8fbfae2b95fafe71a309fcfbb7c1c993f16ad8`. The fixed codeload archive has
SHA-256 `dd6fd2b62ef20e12dd282e3bf41b72ed9641b5f0cfe3a25276ac672651bfd5a4`;
all 38 source Git blobs were verified. RPM version follows the official `0.3`
tag; upstream's unchanged configure/API and pkg-config version is `0.3.0`.
Frozen Fedora `0.3-21.fc44` and openSUSE `0.3-2.5` are discovery lineage, not
executed recipes or target-build evidence. Complete official/supplemental target
name and file lists showed no libcircle package, header, SONAME or pkg-config
collision at intake; provider availability is not a DNF transaction proof.

`LicenseRef-LANL-BSD` means the exact LANL/Government-rights and BSD-style terms
in this commit's `COPYING`, not an assumed SPDX equivalence to LBNL's license.
The MPI macro's LLNL/Libra BSD-3-Clause notice and the FSF unlimited-copying
notice (FSFAP) in `m4/ltsugar.m4` are retained in full alongside `COPYING` as
installed license payloads. This declaration includes build-support notices.

MPI remains mandatory. The official target providers are pinned to
`openmpi-devel = 4.1.5-7.oe2403sp3` and `check-devel = 0.15.2-2.oe2403sp3`;
`libxcrypt-devel = 4.4.36-3.oe2403sp3` keeps their SP3 glibc-static closure
compatible rather than selecting the incompatible newer supplemental provider.
Do not mix OpenMPI and MPICH. Build and development-test dependencies use the
same pins. Exact locked target CI must still prove dependency installation.

## Tests and declaration-only patch

Upstream Travis's `--enable-tests`, complete `make check`, strict default
`common.mk` flags and default shared/static libraries are retained. Upstream
registers one Check executable containing four queue cases; the commented-out
checkpoint test is not registered and is not counted. The sole patch adds
`stddef.h` to two headers using `size_t` and `string.h` to the original test using
string functions. It changes no function body, case, assertion or compiler flag.
This generic modern-C declaration fix comes from inert source inspection, not
an observed target execution or a RISC-V-specific failure. It was not submitted
upstream; remove it when an official release contains equivalent declarations.

Staged and installed replays compile the same four original cases with `mpicc`
against shared/static libraries at `-O0`/`-O2`, verify fixture checksums, actual
shared-library resolution, and embedded runtime-path safety. These are
repetitions, not extra unique tests. Keep Check's default per-case fork isolation
because each case initializes/finalizes MPI. The 120-second per-case and
600-second suite bounds accommodate QEMU; expiry fails rather than skips.
Singleton queue/MPI initialization tests do not establish distributed multi-rank
correctness, network behavior, performance, native timing or native RVA23 proof.

Exact-head CI run `38841227360` passed all four original queue cases, then the
packaging replay failed because the pinned SP3 `mpicc` wrapper adds the absolute
RUNPATH `/usr/lib64/openmpi/lib`. This is a package test-driver contract error,
not an upstream/RISC-V defect. The replay now permits exactly that audited
provider path (or no embedded path), while still failing empty paths, path lists,
relative/build-root/temporary paths and every other embedded directory. Actual
libcircle resolution and all original tests remain mandatory. No source or
assertion changes are involved; the replacement head still needs fresh target
build/install and physical-product acceptance.

No local source execution, RPM/QEMU build or install was performed during
intake. Source/schema verification and trusted repository tests are distinct
from pending exact-head target build/install and physical RPM/SRPM acceptance.
No auto-merge or publication is enabled by this package.
