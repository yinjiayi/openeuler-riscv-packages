# wget2

This package tracks the official GNU Wget2 2.2.1 stable release for
openEuler 24.03 LTS SP3 on RVA23 riscv64. The GNU release archive is pinned
by SHA-256, the `libwget.so.4` ABI is packaged separately for consumers, and
the complete serial upstream test suite is enabled with its local HTTP/TLS
test dependencies. If that complete suite fails, its test-suite log is emitted
to the CI build log for exact package-level diagnosis; no tests are skipped or
ignored.

Packaging release 3 keeps libproxy-based desktop and PAC discovery enabled,
but applies explicit HTTP/HTTPS proxy and no-proxy settings first. This fixes
the three IDN integration tests that otherwise bypassed their local test proxy
and attempted external DNS resolution when libproxy support was compiled in;
the complete upstream test suite remains unchanged.
