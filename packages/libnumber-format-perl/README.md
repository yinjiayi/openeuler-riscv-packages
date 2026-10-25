# Number::Format

`libnumber-format-perl` packages the official stable Number::Format 1.79
release as `perl-Number-Format` for openEuler 24.03 LTS SP3, riscv64/RVA23.
The frozen inventory's Ubuntu `1.76-1` is discovery lineage, not the chosen
release. Authorized uploader RJBS's latest stable MetaCPAN record, official
HTTPS archive and author CHECKSUMS agree on 43,273 bytes and SHA-256
`404b231709b28a41024ae76bedd349145da7e535f94c6013b6bb55eea383e1ad`.
Archive, RPM and unchanged direct module VERSION are all 1.79. Actual main
paths/RPM/module aliases, all OPEN PR package paths and checksum-bound
official target primary were screened before onboarding; absence is not
inferred from the frozen inventory's status alone.

All 29 safe ordinary archive members/24 regular files were read, including
the complete module/POD, generated metadata/release helpers, all tests and
historical contributor credits. Original source bytes, modes and features
remain unchanged; there is no source repack or patch. Module and README
explicitly grant Perl 5 terms under William R. Ward's original copyright;
the full bundled LICENSE supplies GPL-1.0-or-later and ten-clause
Artistic-1.0-Perl alternatives. Original LICENSE, README and Changes are
installed as license files, preserving the grant, terms and credits. This
is a bounded observed-notice review, not a legal-certainty claim. No
detached signature is advertised or verified; `signature: null` is honest.

## Default tests and dependencies

The generated upstream Makefile runs all ten `t/*.t` files through Harness;
that default `make test` is retained. A second explicit Harness pass must
have ten complete files, 183 assertions, zero failures, skips, TODO or bonus
results and empty failed/TODO maps. The number 183 is a static expectation
from the unchanged suite, not observed target success before CI. Original
locale tests require German, Russian and US English data and otherwise
skip assertions. BuildRequires `glibc-all-langpacks` supplies physically
verified `de_DE.utf8`, `ru_RU.utf8` and `en_US.utf8` data; actual POSIX locale
activation is prechecked in CI, with a C reset, without editing tests or
forcing module settings. Complete default-suite acceptance still depends
on current-head target CI showing the strict zero-skip result.

MakeMaker >=6.78, Test::More >=0.96, all runtime/default-test modules and
Harness are explicit prechecks: the upstream `00-report-prereqs.t` only
prints diagnostics and passes, so is not used as dependency proof. All
providers are available in checksum-bound official target primary.
The three `xt/author` and `xt/release` files remain unchanged in Source0/SRPM
but are developer/release checks excluded by upstream default `t/*.t`;
neither those checks nor Dist::Zilla release tooling are claimed executed.

Installed smoke verifies the real module/provider version, original module
and three notice hashes, plus rounding, grouping/fill, custom separators,
negative formatting, monetary placement, pictures/overflow, IEC and
traditional byte quantities, parsing and invalid-input failure behavior.
It uses C locale and explicit formatting configurations; it does not test
installed non-C locale data. Thus large `glibc-all-langpacks` is a build-test
dependency, not a fabricated runtime requirement. Local work executes only
repository validation/tests/golden/dashboard and source verify-only,
never upstream tests or RPM/QEMU builds. Hosted current-head artifacts
remain required; no native, performance or publication success is inferred.
