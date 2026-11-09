<!-- SPDX-License-Identifier: Apache-2.0 -->
# File::Tempdir 0.02

Noarch Perl object interface to File::Temp for openEuler 24.03 LTS SP3,
riscv64/RVA23. A managed object deletes the temporary directory it creates;
a user-supplied directory remains owned by the caller.

The fixed official CPAN archive matches MetaCPAN and the author's CPAN
CHECKSUMS. The frozen Fedora 44 lineage is perl-File-Tempdir 0.02-30.fc44;
the official Fedora package page confirms that build. No distro recipe was
executed. The direct grant in the shipped File/Tempdir.pm POD says the same
terms as Perl itself, even though MetaCPAN classifies the legacy metadata as
unknown. The SPEC installs an unmodified excerpt of the original POD containing
the author attribution and the entire grant. No external generator is bundled.

The SPEC runs the complete original default `make test` (8 assertions) with
temporary paths isolated in the package build tree. Installed smoke verifies
creation, destruction and preservation of caller-owned directories. No source
patch is needed. Host tests do not substitute for target RPM/install evidence.
