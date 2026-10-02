<!-- SPDX-License-Identifier: Apache-2.0 -->
# Time::Tiny 1.08

The frozen `libtime-tiny-perl` inventory key and Debian source package
`libtime-tiny-perl` 1.08-3 map to official stable
[Time-Tiny 1.08](https://metacpan.org/dist/Time-Tiny). Publisher CHECKSUMS and
the independently downloaded 19,681-byte HTTPS archive agree on SHA-256
`00f7b231dedf170067903584c6e9b5e3ae9d11c4a66ac20ce0eb3d38b7d19282`.
The archive has a single top-level tree and contains no vendored code.

The installed `lib/Time/Tiny.pm`, README and bundled LICENSE directly grant
same-as-Perl redistribution by Adam Kennedy; default tests and their generated
prerequisite data contain no contrary notices. The RPM license expression
records Perl's GPL version 1-or-later or Artistic choice. The upstream `xt/`
author/release checks are not part of the default `t/*.t` suite.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Time-Tiny` package or module provider. It supplies Carp, overload,
ExtUtils::MakeMaker, File::Spec, Test::More and DateTime 1.58 with Locale 1.35
and TimeZone 2.62; the DateTime provider dependency closure was checked. The
two original default test files locally passed 16 assertions, including all
seven optional DateTime assertions, without skips. The first target run
`37061993495` failed only locale assertion 11: SP3 DateTime::Locale 1.35
canonicalizes `C` as `en-US`, but the upstream version heuristic expected
`en-US-POSIX` for every version at least 1.00. Independently executed
official upstream DateTime::Locale 1.35 returned `en-US` from both
`load('C')` and a DateTime constructor; local 1.25 returned
`en-US-POSIX`. The package-local test patch keeps all 16 assertions and
compares to a concrete expected value for each version range rather than
deriving the expected value from the constructor. The first target run
produced no RPM/SRPM or installed smoke evidence. A new exact-head CI run
must prove the complete suite, physical RPM/SRPM, DNF installation and
installed time-object roundtrip. DateTime is a hard build dependency to
exercise the upstream conversion branch, but remains an optional runtime
integration as upstream
declares it. No local RPM or QEMU build was run, and PR CI is not repository
publication.
