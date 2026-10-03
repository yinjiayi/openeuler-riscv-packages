<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-statsd-perl

The frozen inventory lists Debian `libnet-statsd-perl` 0.12; Debian trixie
carries 0.12-4. The current official COSIMO CPAN release 0.13 is also carried
by Debian sid as 0.13-1 and includes the CVE-2026-46739 malformed-metric
regression test. `Net-Statsd-0.13.tar.gz` is 20,310 bytes, SHA-256
`c4a60ff5d3f4d36a26a6a477631188ec79cdce9e3050c67a34e9b5ae2920a100`,
matching the publisher's `CHECKSUMS`. The single-root archive has regular
files only, no vendored code or third-party dataset. Its `LICENSE` and
`README` grant the full distribution the same terms as Perl 5, consistent
with the module POD and metadata; RPM selects GPL-1.0-or-later, one explicit
alternative. The license remains in the SRPM and installed RPM.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither a `perl-Net-Statsd` RPM nor a `perl(Net::Statsd)` provider. It does
provide Perl, `perl(IO::Socket)`, `perl(IO::Socket::INET)`, `perl(IO::Select)`,
`perl(Carp)`, `perl(File::Spec)`, `perl(File::Basename)`,
`perl(Time::HiRes)`, `perl(Test::More)` and
`perl(ExtUtils::MakeMaker)` for all declared runtime/build/test paths. This
is a repository snapshot check, not a guarantee about later state.

All four original `t/*.t` files remain unchanged. Source-only local `prove`
passed 41 assertions without skips: module load, localhost UDP mock server,
sampling regression, and malformed-metric rejection. Target `%check` runs
the same complete default suite. Installed smoke verifies an actual UDP
counter packet on loopback and the injection guard. The upstream benchmark
script is retained as `net-statsd-benchmark` to avoid a generic executable
name collision, but it is not used as native RISC-V performance evidence.
QEMU-user functional results cannot prove native RISC-V timing, performance,
or public repository publication.
