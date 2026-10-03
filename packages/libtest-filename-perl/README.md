<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-filename-perl

This package maps the frozen Ubuntu `libtest-filename-perl 0.03-3` lineage
to DAGOLDEN's official CPAN `Test-Filename-0.03.tar.gz` release. Its SHA-256
`6a450cc4c6281ed1129f32a1c0741f228967feda2e32a2915ff621c36525fcbe`
matches the publisher's `CHECKSUMS`. The archive contains only regular files
and directories beneath one root, with no separately vendored code. The
archive `LICENSE`, module POD and `dist.ini` consistently identify
Apache-2.0; the remaining test, example, metadata and documentation files
are part of that same distribution and carry no conflicting notice.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither a same-name RPM nor `perl(Test::Filename)` provider. It
provides the declared Path::Tiny and Test::Builder::Module runtime modules
and every default test prerequisite, including Test::Tester. Exact-head DNF
must still prove target closure.

The SPEC uses the unmodified upstream Makefile.PL and runs both original
default `t/*.t` files in `%check`; it does not opt into separate `xt/author`
or `xt/release` suites. Pristine local `make test` passed two files and 27
assertions without skips. Installed smoke checks both filename comparison
functions and the RPM ownership of the loaded module. Pull-request CI is
not public repository publication.
