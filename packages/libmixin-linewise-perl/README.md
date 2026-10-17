# Mixin::Linewise

Official RJBS stable distribution 0.111 supplies Mixin::Linewise::Readers
and Writers. These generate file/string methods around caller-defined handle
methods, using Sub::Exporter and explicit/default encoding layers. The top-level
Mixin::Linewise module is documentation-only: its original code intentionally
throws `not meant to be loaded`. It is preserved, not patched or blindly loaded
by installed smoke.

The frozen Ubuntu `libmixin-linewise-perl` 0.111-1 row is discovery lineage,
not executable packaging or proof of current target availability. Before this
proposal, exact current-main package identities and complete OPEN baseline plus
fresh updated-delta ownership showed no competing package. Checksum-bound
official SP3 RVA23 primary had no Mixin::Linewise/Readers/Writers provider;
this is a metadata snapshot, not a universal installed transaction guarantee.

Source0 is the unmodified official author archive:
`https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Mixin-Linewise-0.111.tar.gz`.
Its 20,120 bytes and SHA-256
`d28e88516ce9b5295c31631dcccdc0fc8f2ab7d8a5cc876bb1b20131087b01db`
agree with authorized/latest/released MetaCPAN API and author HTTPS CHECKSUMS.
All 30 ordinary members/21 regular files and modes were reviewed. No PGP or
cryptographic signature verification is claimed; source identity checks are not
signature verification. No source repackaging, downstream patch or fixture edit.

All three modules use direct version declarations 0.111. Installed smoke requires
their actual three versioned RPM capabilities and checks Readers/Writers runtime
versions; generator correctness still requires actual target CI/RPM inspection.
It hashes the unchanged top-level module without loading its forbidden namespace.

## Rights and notices

Original LICENSE, README and all three module notices explicitly grant
Ricardo SIGNES copyright 2008 under Perl terms. The complete bundled LICENSE
contains GPL version 1-or-later and the generic nine-clause Artistic 1.0 text.
The package therefore records `GPL-1.0-or-later OR Artistic-1.0`; META's
`Artistic-1.0-Perl` identifier is not treated as exact equality with that text.
This accounting preserves the original grant and alternatives, not a relicense
or legal-certainty/historical-ancestry claim. Full unchanged LICENSE/README and
Changes with contributor credits install as license material; smoke hashes them
and all three original modules. Apache-2.0 applies only to original packaging.

## Complete retained tests and scope

Original Makefile.PL selects all four `t/*.t` files, with test helper and numeric
and UTF-8 fixtures intact. Static expected assertions are reader 11 (three input
forms times three reading methods, plus UTF-8 and Latin-3), encoding 3, writer 2,
and prerequisite-report 1: 17 total. The functional files use `done_testing`;
these are static counts, not a claimed executed pass. No original default
skip/TODO branch was observed. Two `xt` author/release files are outside that
default selection and are not claimed passed; the original release test's
conditional Changes skip remains untouched.

`%check` keeps original `make test`, followed by explicit strict Harness totals
for four files/17 assertions and zero skips, failures, TODO or bonus results.
The original prereq report warns then passes; separate fail-closed version/load
guards require MakeMaker >=6.78, Test::More >=0.96 and all original suppliers.
Build uses an unprivileged identity with network-enabled, checksum-bound declared
source retrieval. It never substitutes encodings or removes PerlIO::utf8_strict
or Sub::Exporter to make dependency installation succeed.

Installed smoke uses a fresh private temporary directory for UTF-8, Latin-3 and
raw file/string reading and writing, custom reader generation and intended
invalid-input failures. It checks actual provider/version and original notices.
Named-pipe support is mentioned upstream but not claimed verified here. Neither
local upstream tests/RPM/QEMU execution, target success, native/performance/
permission-security validation, merge nor public publication is claimed before
the corresponding exact-head hosted CI and physical product audit.
