# wget2

This package tracks the official GNU Wget2 2.2.1 stable release for
openEuler 24.03 LTS SP3 on RVA23 riscv64. The GNU release archive is pinned
by SHA-256, the `libwget.so.4` ABI is packaged separately for consumers, and
the complete serial upstream test suite is enabled with its local HTTP/TLS
test dependencies. If that complete suite fails, its test-suite log is emitted
to the CI build log for exact package-level diagnosis. The package adds no test
skips or ignored failures. Upstream itself returns skip status77 for 17 fuzzers
whose .in and .repro corpora are absent from the official source release.

Packaging release 3 keeps libproxy-based desktop and PAC discovery enabled,
but applies explicit HTTP/HTTPS proxy and no-proxy settings first. This fixes
the three IDN integration tests that otherwise bypassed their local test proxy
and attempted external DNS resolution when libproxy support was compiled in;
the complete upstream test suite remains unchanged.

Packaging release 4 accounts for the complete install manifest observed on
RVA23: it ships the generated Wget2 manual and removes the upstream
`wget2_noinstall` test helper from the build root. The preceding exact-head CI
run's integration summary completed 83 cases with zero skips before RPM's
unpackaged-file check identified those two manifest entries. That summary is not
the complete suite count: current full logs show 20+5+83=108 total cases,
3+5+83=91 passed, and 17 original missing-corpus skips. No full fuzzer-corpus
coverage or complete zero-skip claim is made.

Packaging release5 repairs independently observed installed legal incompleteness,
without changing source logic, proxy patch, build configuration or complete
serial `make check`: full original GPL3/LGPL3 and full official GNU FDL1.3 texts
are installed with every subpackage. The installed smoke verifies their exact
hashes, retains the libwget compile/link consumer and performs an explicitly
downstream deterministic loopback HTTP payload comparison. This is maintenance
of a product-acceptance defect despite green CI, not a fabricated CI failure.
Replacement exact-head hosted build/tests/install and independent physical
RPM/SRPM/legal payload acceptance remain mandatory before merge. No local
upstream/RPM/QEMU execution, native/performance/security claim, test suppression
or automatic merge is authorized by this change.
