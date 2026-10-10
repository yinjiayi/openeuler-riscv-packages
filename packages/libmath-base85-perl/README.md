# Math::Base85

Math::Base85 converts arbitrary-precision integers to/from the RFC 1924 base85
alphabet. Frozen inventory Ubuntu `libmath-base85-perl` 0.5+dfsg-2 and its
Arch/Fedora/MetaCPAN aliases identify the same upstream component. The `+dfsg`
distribution source is lineage only, not the source used here or proof of rights.
The actual current-main package paths, RPM names and module aliases have no
equivalent package. Official target primary SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a` supplies
neither `perl-Math-Base85` nor `perl(Math::Base85)`: this is missing target
coverage, not a version uplift. All declared runtime/default-test dependencies
are available, including Math::BigInt, Test.pm, Test::More and MakeMaker >=6.64.

## Exact source and distinct rights

The [official stable CPAN archive](https://cpan.metacpan.org/authors/id/P/PT/PTC/Math-Base85-0.5.tar.gz)
is 10,316 bytes, SHA-256
`0b05f7fb650a8797b392d8ea90f2e72bfb8d08505c9a2e0b955dfd45a72a34e5`, matching
[author CHECKSUMS](https://cpan.metacpan.org/authors/id/P/PT/PTC/CHECKSUMS) and
[MetaCPAN's authorized stable API record](https://fastapi.metacpan.org/v1/release/Math-Base85).
All fifteen safe archive entries and eleven complete regular files were reviewed.
No detached signature is declared or signature verification claimed. Source0,
all file bytes/modes, RFC, original copyright/disclaimers and tests remain intact,
without repack or patches.

The actual Math::Base85 grant is in the original module and README: Tony Monroe
2001–2002 and Paul Cochrane 2017 offer Perl terms, excluding the RFC from that
software grant. This packaging selects the [Artistic-1.0-Perl](https://spdx.org/licenses/Artistic-1.0-Perl.html)
alternative whose complete ten-clause text is supplied. The original upstream
Perl dual-license grant, including its GPL alternative, is not changed or
relicensed. The supplied LICENSE has a stale introductory line naming
Module::Release; that line is not presented as Math::Base85's grant and is not
rewritten. Original module/README copyright notices remain authoritative.

`LicenseRef-RFC-1924-Verbatim` is a local license-accounting identifier for the
separate full original RFC 1924 and its explicit unlimited-distribution notice.
It is not an SPDX-listed license, a general modification grant or the code's
Artistic license. The bundled six-page document, Robert Elz's April 1996
RFC, is byte-identical to the [official RFC-editor text](https://www.rfc-editor.org/rfc/rfc1924.txt):
10,409 bytes, SHA-256
`a7a388e155294a60ab16d857dcbb6bb50fa5c954001398d67ae7c8aa2a63229c`.
The [IETF Trust's reproduction FAQ](https://trustee.ietf.org/about/faq/) describes
permission to reproduce whole RFCs, while retaining author rights and noting
possible objections to particular commercial republications. This package uses
only whole-verbatim document distribution with all original authorship/notices.
RFC 1924 is an April 1 Independent Stream RFC from 1996, predating the modern
2009 Independent Stream rules. This route relies only on the original document's
whole-verbatim distribution notice, not retroactively inferred derivative rights
under later policies.
No broad derivative permission, public-domain status, DFSG/FLOSS qualification,
blanket commercial clearance or legal certainty is claimed. The numeric test
vector is retained, without importing or modifying RFC prose into the code.

SPEC installs the original LICENSE, original README.md grant and full original
rfc1924.txt as `%license`, so `--nodocs` does not remove those notices. Installed
smoke verifies all three exact file SHA-256 values. No upstream contact or write
is performed.

## Tests and evidence boundary

The complete default `t/00-basic.t` and all five Test.pm assertions remain;
upstream `make test` uses Test::Harness and must fail on unsuccessful TAP. No
test/fixture/feature is skipped or weakened. Installed smoke additionally checks
the provider/version, zero conversion, original RFC numeric vector, roundtrips
and invalid-digit rejection, exiting nonzero on any failed check.

Local work is source verify-only plus repository metadata/unit/Golden/Dashboard
checking, not local upstream builds/tests or RPM/QEMU execution. Fresh exact-head
hosted target CI must establish default tests, installation/smoke, complete
structural records and physical source/RPM/SRPM evidence. No native RISC-V
validation, protected-main build or public RPM/SRPM publication is claimed;
CI artifacts are not public package repository addresses.
