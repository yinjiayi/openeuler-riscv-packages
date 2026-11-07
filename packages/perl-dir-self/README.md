<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-dir-self

This directory packages upstream `https://metacpan.org/dist/Dir-Self` version `0.11` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed official CPAN archive is
`https://cpan.metacpan.org/authors/id/M/MA/MAUKE/Dir-Self-0.11.tar.gz`,
SHA-256 `e251a51abc7d9ba3e708f73c2aa208e09d47a0c528d6254710fa78cc8d6885b5`.
The downloaded bytes match both MetaCPAN release metadata and MAUKE's CHECKSUMS
index. The available index signature verifies with SHA-512 and PAUSE signing
subkey `4584D789E682F9F53B392F1837D079412CC9032E`, bound to primary
`2E66557AB97C19C791AF8E20328DA867450F89EC` published at
`https://www.cpan.org/modules/04pause.html`. This is signed-index evidence,
not an archive detached signature; `sources.yaml` requires the archive digest
and records the index signature as advisory.

Discovery lineage is Debian stable (trixie) `libdir-self-perl` 0.11-4:
`https://packages.debian.org/trixie/libdir-self-perl`. Debian packaging was not
executed or copied. Current managed directories, all open PR titles/files and
official/supplemental target Provides/file namespaces were checked for aliases
including `Dir::Self`, `Dir/Self.pm`, `perl-Dir-Self` and `libdir-self-perl`.

The module's explicit copyright/license permits the same terms as Perl 5.8.8
or any later Perl 5 (GPL-1.0-or-later OR Artistic-1.0-Perl). Makefile.PL also
declares `LICENSE => 'perl'`; no bundled third-party build helper is present.
The module license text is retained in the installed license directory.

The unmodified upstream `make test` suite runs all three assertions, including
the nested `t/zerlegungsgleichheit/d.t` helper. Nothing is removed or skipped.
It passed on the macOS Perl host only; target RPM build, original tests,
installation and smoke remain CI gates, not inferred from host execution.
The smoke test checks the installed version and dynamic/static directory
imports. MakeMaker uses only declared target-supplied Perl/core/test tooling;
there is no automatic CPAN installation or build-time networking. No patch
or RISC-V-specific limitation is known; this pure-Perl package uses the normal
QEMU-user target CI profile and is not native-hardware validation.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
