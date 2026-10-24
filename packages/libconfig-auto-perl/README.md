# Config::Auto 0.44 for openEuler RISC-V

This package proposes the official BINGOS stable release for openEuler 24.03 LTS
SP3, riscv64, RVA23. Local metadata and inert source verification do not establish
target build, installed-RPM acceptance, native verification or publication.

## Source and scoped notice accounting

`sources.yaml` pins the original 16668-byte Config-Auto archive with full SHA-256.
All 22 original files, modes, MANIFEST entries, contributor notices and default
tests remain unchanged; there is no source patch or archive repack.

The library's original same-Perl grant and README AL&GPL grant remain dual
GPL-1.0-or-later OR Artistic-1.0-Perl. Its copied Makefile.PL `WriteMakefile1`
version 0.21 is separately credited to Alexandr Ciornii and matches the official
CHORNY App-EUMM-Upgrade 0.21 template after only CRLF-to-LF conversion. The source
aggregate additionally accounts for this GPL-3.0-only helper. This does not label
the entire runtime GPL3-only or claim a legal determination.

Four fixed HTTPS supplements preserve the whole 2078-byte origin module notice,
complete GNU GPLv3 text and both complete Perl terms at immutable official Perl
commit 76298ae68aa7796f0ffc05095b127d23f4b2de8f. They are full notice documents,
not generator/inc code imported for execution. The initial GNU TLS failure is
retained in local evidence; a later fresh normal-TLS HTTP200 matched all four
full digests. Historical source review or HTTP availability is not CI success.
The license-source version 5.38.0 refers to the official Perl v5.38.0 tag,
whose annotated tag f47267bec5921b10a8cc16545c9fdf11972c5f2d points to this
commit; the unsigned tag is an identity reference, not signature authentication.

## Complete target test gate

Build and tests run as UID/GID 10001 with a private0700 HOME. Network-enabled CI
retrieves only declared pinned source bytes, verifying SHA-256 before rpmbuild.
The original `perl Makefile.PL -x` XML feature is enabled without altering source.
Real XML::Simple, YAML::Any>=0.67, Config::IniFiles and Test::Pod>=1.14 must load;
bundled t/fstab and the deliberate negative XML fixture must remain present.

The unmodified MakeMaker default suite runs first, then a strict repeat over all
ten original t/*.t files. Nine functional suites statically total 378 assertions;
the POD plan is dynamic and exact total must be observed in CI. Strict totals
require ten successful files, all assertions positive, at least379 assertions,
and zero failures, skips, TODO or bonus. The mock t/lib/XML/Simple.pm remains
confined to the original negative XML test, not positive parsing prerequisites.
Literal full SHA-256 guards verify all 22 original files and four supplements
after preparation, before building/checks and after checks. No original source
or default test is rewritten to satisfy a guard.
Original unavailable bind/irssi methods and Perl configuration eval/DisablePerl
semantics remain intact; no feature deletion or security-sandbox claim is made.

Installed smoke uses a private ordinary-user directory, verifies original module
and full notice hashes, and exercises supported parsing plus explicit original
unsupported formats and DisablePerl refusal. Actual module version Provide,
RPM/SRPM source payload, default TAP and installed smoke must be independently
verified on the exact hosted CI head. This package has no published product URL
until protected-main trust, build and public generation evidence are verified.

## Static dependency boundary

The complete official 18503-package RVA23 primary and same-generation 1192-package
supplemental primary contain exact providers for source imports, enabled XML,
YAML/INI, Test::Pod and Harness 3.48, plus packaging and smoke tools. The official
compressed primary was freshly retrieved and its compressed/open SHA-256 checked
against current official repomd; the supplemental cache was rehashed against
unchanged public-generation metadata. Neither index has an existing exact
perl-Config-Auto RPM or perl(Config::Auto) Provide. These are static supplier
observations, not dependency-transaction success or installed module evidence.
Harness statistics are checked against the complete official RPM's byte-bound
Test/Harness.pm 3.48 implementation; target execution remains required.
