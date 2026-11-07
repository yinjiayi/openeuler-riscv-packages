<!-- SPDX-License-Identifier: Apache-2.0 -->
# aliased 0.34

This package provides `perl-aliased`, the pure-Perl pragma for short class
aliases. The canonical directory follows the frozen Ubuntu source-package
lineage `libaliased-perl` (0.34-3), not a distinct upstream component.

## Source and license

The official CPAN stable release is pinned in `sources.yaml` to SHA-256
`c350524507cd827fab864e5d4c2cc350b1babaa12fa95aec0ca00843fcc7deeb`.
The downloaded 30,464-byte archive matches its publisher's
[`CHECKSUMS`](https://cpan.metacpan.org/authors/id/E/ET/ETHER/CHECKSUMS).
MetaCPAN identifies 0.34 as the current released version. No detached archive
signature is supplied. The signed CHECKSUMS index was additionally verified
at intake: its SHA-512 signature uses subkey
`4584D789E682F9F53B392F1837D079412CC9032E`, cryptographically bound to the
[official PAUSE primary key](https://www.cpan.org/modules/04pause.html)
`2E66557AB97C19C791AF8E20328DA867450F89EC`. An updated certificate supplies
current self-signatures and expiration; the keyserver is only a source of
certificate bytes, not the trust anchor. This verifies the index containing
the archive digest, not an author-created detached archive signature.
The included `LICENSE` grants the GPL version 1 or later, or the Artistic Perl
license, and supplies both license texts. No external packaging recipe is used.

## Target and dependencies

The target is openEuler 24.03 LTS SP3 riscv64/RVA23. The official target indexes
checked on 2026-11-07 supply Module::Build::Tiny 0.047 (required >= 0.039),
ExtUtils::MakeMaker 7.70, Test::More 1.302198, CPAN::Meta 2.150010, and the
Perl RPM generators. Core Perl supplies the runtime dependencies.
The official and supplemental provider/file indexes and all open PR package
paths were checked for `aliased`, `perl-aliased`, `libaliased-perl`,
`perl(aliased)` and the installed `aliased.pm` namespace; no collision was found.

## Tests and patch policy

The original `Build.PL`, `perl Build`, and complete default `perl Build test`
are used without exclusions or environment switches. Upstream's separately
opt-in author/release tests under `xt/` are not made default tests here.
No source patch is required. Installed smoke verifies loading, explicit class
aliasing, class-method dispatch, and the prefix API from the installed module.

Local source verification and repository fixture tests do not establish a
target RPM build. Exact-head CI must still build the RPM/SRPM, run the original
tests, install the package and pass installed smoke before merge admission.

External source licenses remain upstream's; Apache-2.0 covers only original
packaging metadata, scripts and documentation in this directory.
