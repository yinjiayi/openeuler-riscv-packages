<!-- SPDX-License-Identifier: Apache-2.0 -->
# accessors 1.01

This package provides `perl-accessors`, the compile-time Perl accessor-method
generator. Canonical directory `libaccessors-perl` retains the frozen Ubuntu
source-package lineage (1.01-4), not a separate upstream component.

## Official source and licensing

The official CPAN 8,650-byte archive has SHA-256
`3a8db00f38148f3afadbe5330dc5490d9933f9cae137e842ec225a4d3adb2d9f`,
matching the exact publisher CHECKSUMS entry. Current official MetaCPAN metadata
identifies 1.01 as the stable released version.

Author Steve Purkis explicitly declares `license => 'perl'` in the original
`Build.PL`; original `META.yml` corroborates `license: perl` and links the
official Perl license terms. These original declaration files are installed
as license evidence. Upstream does not supply a standalone license text, and
none has been invented. The source archive contains this module family and
its tests, with no bundled third-party library or font assets. No external
distribution packaging recipe is used.

No detached archive signature is supplied. The source SHA-256 remains
mandatory. The signed CHECKSUMS index is explicitly advisory: GPG reports
a mathematically valid 2021 SHA-1 signature from historical signing subkey
`33EAEF6DBA3865943BEE9D5BB6A1739063760CCA`, but that subkey is expired.
This is not current strong-signature verification. The advisory fingerprint
in `sources.yaml` identifies the official PAUSE primary trust anchor
`2E66557AB97C19C791AF8E20328DA867450F89EC`, published at
<https://www.cpan.org/modules/04pause.html>; it does not assert a required
detached-signature verification result or weaken a previous required policy.

## Target, tests and patch policy

The target is openEuler 24.03 LTS SP3 riscv64/RVA23. Refreshed official and
supplemental indexes on 2026-11-07 supply Perl 5.38.0, Module::Build 0.42.34
(required >= 0.20), Test::More 1.302198 and perl-generators. All managed
directories and current open PR canonical paths, RPM/module names and actual
Perl module/manpage namespaces were screened; no collision was found.

The original `Build.PL`, `perl Build`, and full `perl Build test` are preserved.
Upstream's default suite plans 59 tests across seven files; 18 benchmark-only
assertions are opt-in through `BENCHMARK_ACCESSORS` and remain unchanged.
The recipe neither excludes tests nor sets that environment variable. No
source patch is required. Installed smoke checks all module loads, chaining,
classic accessors, read-only behavior and getter/setter semantics.

Source verification and host-language tests are not target RPM evidence.
Exact-head CI must build the RPM/SRPM, run the original default tests, install
the package and execute installed smoke before any merge admission.

External source licensing remains upstream's; Apache-2.0 covers only original
packaging metadata, scripts and documentation in this directory.
