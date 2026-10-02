<!-- SPDX-License-Identifier: Apache-2.0 -->
# Set::Tiny 0.06

The frozen Ubuntu `libset-tiny-perl` 0.06-1 inventory key maps to official
stable [Set-Tiny 0.06](https://metacpan.org/dist/Set-Tiny). Publisher
CHECKSUMS and the independently downloaded 21,595-byte HTTPS archive agree
on SHA-256
`1e4621e6fa0931231fbcb211a140b54fc30e64cc453644605d830237364d4d33`.
The archive contains only regular files and directories beneath one top-level
tree.

The bundled `LICENSE` grants distribution-wide redistribution under Perl's
GPL version 1-or-later or Artistic License choice by copyright holder Stanis
Trendelenburg. Installed `lib/Set/Tiny.pm` POD, README, `dist.ini`, and META
repeat that grant or its exact SPDX expression. The archive credits prior
contributors but bundles no separate third-party code library.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Set-Tiny` package or `perl(Set::Tiny)` provider. It supplies unique
providers for ExtUtils::MakeMaker, Test::More, File::Spec, IO::Handle,
IPC::Open3, and CPAN::Meta/Prereqs. Hard-requiring CPAN::Meta exercises the
upstream prereq report's verification branch.

The unchanged default `t/*.t` suite has four files and 68 assertions; a
fresh local Perl run passed with no skips. The `xt/` author/release tests are
not invoked by upstream's default `make test` and remain untouched. Target
CI must prove all four default files, 68 assertions, zero skips, physical
RPM/SRPM products, DNF installation, and installed membership and set
algebra smoke. PR CI is not repository publication.
