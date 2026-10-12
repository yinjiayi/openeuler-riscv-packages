<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Measure 0.10

Frozen Debian `libclass-measure-perl` 0.10-1 lineage maps to the official
stable CPAN release. The 14,285-byte BLUEFEET archive SHA-256
`c0b79eb09a66cc41fb83aadbd24874372b465a74407b96e0722994eefbfd24ca`
matches the publisher's `CHECKSUMS` file.

The top-level `LICENSE` grants same-as-Perl redistribution for “This
software,” covering the release archive. `README.md` and both installed
modules repeat the grant. They acknowledge Roland van Ipenburg as a
contributor; there is no contrary file notice or vendored code. The RPM
license expression records the GPL-1-or-later or Artistic-1 choice. This
is a distribution-wide grant, not an inference solely from metadata.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has
no `perl-Class-Measure` name or `perl(Class::Measure)` provider. It has
Module::Build::Tiny 0.047, Sub::Exporter 0.990, Test2::V0 0.000155 and
the remaining hard dependencies. The unmodified four-file default suite
passed 29 assertions locally without skips. Target CI must repeat all
four files/29 assertions, build a physical RPM and SRPM, install through
DNF, and run conversion plus non-mutation smoke using the installed
vendor modules. No local RPM/QEMU build or publication occurred.
