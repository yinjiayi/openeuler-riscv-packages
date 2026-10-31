# Cgreen
Official 1.7.0 at feeb85ed48d163f6b7b0011a6d8e6043951541e4, fixed HTTPS
archive SHA-256 a9b9b5b9215a3774f16c98466644e092767d04deb7d250f1d1e7c8851541e70f.
Debian 1.7.0-1 supplies discovery lineage, not a claim that a target RPM exists.

Retain default shared library, both XML reporters, all original build targets
and full unfiltered original CTest. Fail if libxml2 support silently falls back.
Installed replay uses unchanged tests/CMakeLists and original C/C++ test files
and output expectations, linked to actual installed library and runner.
Run 39132505767 passed all 30 original CTest cases, then exposed a downstream
replay include-path error for the non-installed internal cgreen/messaging.h.
Replay now keeps installed headers first and adds the original source include
tree as fallback. It first byte-compares all 35 headers in the upstream Linux
install lists against their installed copies, so fallback cannot hide a missing
or modified installed public/internal header. No upstream source, test, expected
output, feature, compiler assertion flag or timeout is changed. The replacement
target build and installed replay must pass before this repair is accepted.
Tools-directory tests are full-build-only; public API fixtures are compile-only.
Original intentional nested failures and functional timeout tests are preserved;
this is not native hardware, timing, performance or reliability certification.

License audit: root ISC and CMake BSD-3-Clause notices are retained. The root
ISC copyright template is preserved without inventing an upstream holder; Debian
attributes Cgreen Development Team and contributors, 2006-2022. The original
inttypes.h permissive grant is retained verbatim under LicenseRef-Chemeris-2006:
its clause 3 says “may be used” (no “not”), so it is not silently labelled the
standard BSD-3-Clause text. gopt.c, gopt-errors.c and gopt.h preserve Tom
Vajzovic's explicit public-domain abandonment and warranty warning under
LicenseRef-Public-Domain. Full original source archive, notices and modes remain
in the tests package. No Debian packaging is imported or source test rewritten.

Hosted target build, normal installation and physical product verification are
still required before merge. Local validation does not claim target success.
