# Class::Can 0.01

Inspect Perl class methods and their defining packages. Pure Perl, noarch for
openEuler 24.03 LTS SP3 riscv64/RVA23; no architecture workaround.

## Fixed source and licensing

Official source: https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Class-Can-0.01.tar.gz
SHA-256 `084fa3ad14a06b979c19d13d4644e2cd99370aaa920a44499ba356af23793659`,
1,772 bytes, freshly matched against official release metadata and PAUSE
CHECKSUMS. The publisher index has a mathematically valid historical SHA-512
signature with an expired signing subkey under official primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. It is advisory index evidence, not
a current-valid or detached archive signature. Archive SHA-256 is mandatory.
Fedora perl-Class-Can 0.01-46.fc44 is discovery lineage only; no recipe executed.

The original module retains Richard Clamp's 2004 same-Perl grant. The generated
traditional Makefile.PL was exactly matched to Module::Build::Compat 0.03 in
the official Module-Build 0.25 archive (SHA-256
`cfda8575e400bf42fab7ad05eb7bffeeff1f51b161a18962c2adfd9a1395b6c8`).
That author's original Build.PL and META.yml explicitly declare the Perl license;
the same source defines that option as permission to copy and redistribute under
GPL or Artistic terms. The notice-only patch adds those exact declarations,
the original Ken Williams author credit and precise source provenance. It does
not invent a copyright year, independent upstream LICENSE, or a generated-code
copyright waiver. No auxiliary archive is added to the SRPM. All seven original
source members, including Makefile.PL and default tests, remain byte-identical.
The added notice and the original module containing its license are installed.

## Dependencies and validation

The source really uses Class::ISA, although upstream metadata omits it; explicit
build/runtime requirements retain that functionality. Devel::Symdump and
Class::ISA are target-supplied. Upstream Perl 5.006 is represented as RPM 5.6.
The traditional EUMM recipe requires no Module::Build at runtime/configure and
does not download dependencies. Manifest networking=false is not a claim of
physical network isolation.

The unchanged default make test runs the original t/can.t: one file, three
assertions on host Perl5.34.1, no skips. Private, fixed-source Class::ISA0.36 and
Devel::Symdump2.18 were used solely for host tests; no global installation or
bundling. The notice patch is checked with GNU patch --fuzz=0, retaining all
original source bytes and original tests. Smoke covers inheritance and overrides.

Source-only/host/repository gates are not target RPM build/install evidence.
Exact-head CI must supply actual build/default-tests/install/smoke and physical
RPM/SRPM acceptance. No local RPM/QEMU build, native-hardware or publication
success is claimed. No auto-merge.
