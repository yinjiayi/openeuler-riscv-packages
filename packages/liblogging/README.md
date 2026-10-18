<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblogging

Packages official `rsyslog/liblogging` v1.0.6 (commit
`7060ca060db626ffc7f3033845901abf6544b1bd`) for openEuler 24.03 LTS SP3,
RISC-V RVA23. The pinned archive SHA-256 remains
`5d235b7da35329d7d13349a4b941a197506a3c47bf8c27758c5e56b51c142c58`.
The complete upstream BSD-2-Clause COPYING is retained in every subpackage.

Two retained BSD-2-Clause patches express the previous GCC declaration fixes
without changing function bodies. The original libtool default builds shared
and static libraries; both archives are shipped by `liblogging-devel`.
The journal, RFC3195, stdlog and man-page features remain enabled.

`%check` retains upstream `make check`, which registers no automated cases,
and the original explicit file-output tester invocation. It additionally
compiles the byte-unchanged released `stdlog/tester.c` against staged shared
and static libraries and replays both default and PID file-output modes.
`liblogging-tests` ships that original source, license, a SHA-256 manifest,
and an Apache-2.0 replay driver, not a compiled test executable.
Installed smoke retains both ABI-major-0 ownership checks and replays the
same original tester against installed shared/static libraries, after
`rpm -V`. The original pc file is unchanged; the static consumer links the
already-required libsystemd explicitly because that file omits Libs.private.

This is QEMU-user file-output/API validation, not native systemd service,
network, hardware, timing, or performance evidence. Local checks are metadata,
trusted tooling, shell syntax and inert source/patch verification only.
Replacement exact-head hosted build/install/RPM/SRPM evidence is still required
before merge; earlier green CI does not validate this repair.
