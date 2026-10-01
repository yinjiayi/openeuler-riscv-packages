<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-binary-interpolation-perl

The frozen inventory's exact `libstring-binary-interpolation-perl` key maps
to official stable CPAN String::Binary::Interpolation 1.0.1. Its HTTPS
archive SHA-256
`c2370dd16ea2a68ce64693e75e70f0d5522acb200f59399e87105c47580acb64`
matches publisher `CHECKSUMS`. All 17 archive entries are regular files or
directories under one root, without traversal or links.

The archived module POD explicitly grants either GNU GPL version 2 or the
Artistic License, with both complete texts in `GPL2.txt` and `ARTISTIC.txt`.
This resolves the frozen `license-blocked` marker for this exact release;
META's `unknown`/`open_source` category is less precise than the source
grant and shipped texts. The RPM declares `GPL-2.0-only OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
open SHA-256 `57be74ba1e5023e98fc645095923f23a3260c3a11c3f4785d89eac353749e84a`)
has no same-name RPM or `perl(String::Binary::Interpolation)` provider,
while `perl(Test::Pod)` and `perl(Test::Pod::Coverage)` are available.
A future repository generation must be checked again before merger.

The unmodified upstream default `make test` has three files: one binary
interpolation assertion, one POD assertion and one conditional POD-coverage
file. Local Perl ran the first two successfully but skipped POD coverage
because Test::Pod::Coverage is absent locally; a local full-suite pass is
not claimed. The SPEC requires both POD dependencies so target CI should
exercise all three, and exact-head CI must report the actual outcome.
The upstream functional test covers only one byte; installed-RPM smoke
additionally checks byte values 00, 44 and ff with nonzero failure.
Source-level staged install yielded the module and manual page listed in
the SPEC. Target RPM build, full default tests and installed smoke remain
unverified until exact-head CI; a PR artifact is not public publication.
