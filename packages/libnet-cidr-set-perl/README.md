# Net::CIDR::Set 0.23

`libnet-cidr-set-perl` packages the official CPAN `Net-CIDR-Set-0.23` release
for openEuler 24.03 LTS SP3 `riscv64` / RVA23. The frozen inventory key came
from Ubuntu `resolute/universe` source `libnet-cidr-set-perl` 0.19-1; it is
lineage evidence, not authorization to trust that distribution's recipe or
source bytes. The newer stable upstream archive is pinned to the SHA-256 in
`sources.yaml`, matching the publisher's `RRWO/CHECKSUMS` entry.

## Rights and scope

The archive's `LICENSE` defines Perl 5 dual terms, and `README.md` plus all
three shipped Perl modules repeat the same-terms-as-Perl grant. `META.json`
explicitly states `Artistic-1.0-Perl OR GPL-1.0-or-later`. The main module
credits Net::CIDR::Lite for copied encode/decode routines; that module's
official POD independently grants redistribution under the same Perl terms.
The remaining default tests and build metadata have no conflicting license
notices. No vendored binary or separate third-party fixture is shipped.

## Target and verification

The checksum-bound official SP3 RVA23 primary lacks `perl-Net-CIDR-Set` and
`perl(Net::CIDR::Set)` providers. It supplies the declared build/test packages
and runtime `perl(namespace::autoclean)`. The original ten `t/*.t` files ran
locally without edits: 225 assertions passed and none skipped. `%check` keeps
that full default suite. The installed-RPM smoke checks IPv4 subtraction and
IPv6 CIDR rendering; only target CI can establish its outcome. No native
RISC-V or performance claim follows from QEMU-user CI.
