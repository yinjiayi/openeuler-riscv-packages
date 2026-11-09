# File::PathList 1.04

This small Perl utility searches an ordered list of filesystem paths for a
relative filename, with optional result caching. It is a lookup helper, not a
filesystem confinement or security-boundary implementation.

## Fixed official source and lineage

Source: `https://cpan.metacpan.org/authors/id/A/AD/ADAMK/File-PathList-1.04.tar.gz`.
SHA-256: `e3e2799f3bceeae4992fe31ea892c34e9141f9237598cfadbc89824ede7a662c`.
Retained frozen discovery lineage includes Fedora44 Everything-source
`perl-File-PathList`1.04-43.fc44 and AUR `perl-file-pathlist`1.04-3.
Current official stable source identity was rechecked independently; no
external packaging recipe was executed. Exact module, RPM, aliases and paths
are checked against the complete PR set and target official/supplemental indexes.

Official CPAN CHECKSUMS is declared signature-advisory, not a detached source
signature. The 2021 PAUSE signature mathematically verifies but uses SHA-1 and
an expired historical signing subkey, so it is not current strong-signature
evidence. Official HTTPS and exact mandatory source SHA-256 remain independent.

## License and bundled helper notices

Adam Kennedy copyright2005-2008 and the original complete LICENSE are retained.
This RPM selects the explicit GPL-1.0-or-later branch of the original dual grant;
it does not relicense the source or remove its alternate Artistic terms.

Eight generated inc/Module/Install helpers match the exact official0.76 source
after only generated POD/#line/blank-line/CRLF normalization:
`https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Module-Install-0.76.tar.gz`,
SHA-256 `4ee768fc46aa1bc9bc82a24800bc36c7d69a5378e481b3ad9a42201cb82e4bdb`.
Patch0 adds NOTICE.ModuleInstall with the original general and per-file copyright
and grant blocks for Brian Ingerson, Audrey Tang and Adam Kennedy. The original
full license remains unchanged. This generic notice restoration changes none
of the24 original files or default tests; it is not RISC-V-specific and should
be removed once upstream includes equivalent complete helper notices.

## Original tests and boundary

The recipe selects the fixed bundled helper explicitly with perl -I.; there is
no auto_install directive or dependency download in Makefile.PL. It runs the
whole original make test. Host preflight passed45 assertions before and after
the additive patch. All three original author-test files keep their upstream
AUTOMATED_TESTING/RELEASE_TESTING and optional dependency conditions; no
downstream flag, filter, or test exclusion is introduced.

The installed smoke looks up the actual installed module and checks cached,
missing, absolute-path and parent-directory cases without modifying host files.
Host tests and source-only checks are not target-build or installed-RPM evidence.
Exact-head CI and physical RPM/SRPM/current-main verification remain mandatory
before explicit merge. No build networking is needed; network_during_build=false
is not an assertion of CI network isolation. Archives are not committed.
