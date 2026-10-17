# Cwd::Guard 0.05

This package targets openEuler 24.03 LTS SP3 riscv64/RVA23, using the locked
QEMU user image, network-enabled source retrieval and ordinary UID/GID10001.
Active update metadata is not target acceptance: exact-head hosted tests,
installed smoke and physical RPM/SRPM evidence are still pending.

## Identity, source and original notices

The immutable discovery component is search.cpan.org-dist-cwd-guard, with
the metacpan.org-release-cwd-guard alias and Debian stable/main
libcwd-guard-perl0.05-4 lineage. Latest authorized official KAZEBURO release
is0.05. Its fixed HTTPS archive is10253bytes, SHA256
7afc7ca2b9502e440241938ad97a3e7ebd550180ebd6142e1db394186b268e77;
release API and author CHECKSUMS agree. One source, no repack or patch:
all12 regular original files/modes, original MANIFEST and tests remain intact.

Masahiro Nagano's same-Perl grant accompanies the module and README. The full
bundled LICENSE permits GPL version1-or-later or the generic nine-clause
Artistic License. This distribution selects Artistic-1.0 as one original
alternative, not a replacement or limitation of upstream's GPL choice.
Install full unchanged LICENSE, README.md, Changes, META.json, META.yml and
Guard.pm as RPM license materials; this preserves upstream grant/disclaimers,
contributor credits (including Aristotle Pagaltzis and Slaven Rezic), and
change history even when documentation is disabled. No complete legal ancestry
or legal certainty is asserted; Minilla-generated packaging metadata is not
proof of an independently audited generator genealogy.

## Preserved default tests and supplier gate

Use original Module::Build Build.PL with vendor installation. The full
original ./Build test remains under a180second deadline plus10second kill
grace, followed by the same3file suite through pinned Harness3.48, Verbose1.
The exact default plans are compile1, basic5 and renamed1 (7assertions).
Strict statistics require files/tests/good3, max/ok7 and every bad, skipped,
sub_skipped, TODO and bonus count0, with empty failed/TODO-success maps.
All counters must be defined unsigned scalar integers. Eight nonempty
Perl/Harness override variables are rejected before default imports/tests.

The original renamed-directory test imports File::Spec::Link via
Test::Requires and otherwise can skip all when original USE_FCHDIR is false.
That original source/guard is unchanged. Declare File::Spec::Link>=0.080 as
BuildRequires and load it before defaults; also require the original module's
USE_FCHDIR constant true. Neither a forced constant nor skipped renamed test
is accepted. The exact provider is supplemental perl-File-Copy-Link0:0.200-1,
whose module capability is0.080. It is a test-only dependency, not a fabricated
runtime requirement. Module::Build>=0.38, original Test::More/Test::Requires,
core imports, Harness3.48 and packaging/smoke tools are present in bound complete
official18503/supplemental1192 metadata; this is not DNF/load/target proof.

## Installed smoke and limits

Smoke drops root to10001:10001 with all supplementary groups cleared. It uses
private mode0700 File::Temp directories, verifies original installed module,
all6 full notice hashes, VERSION0.05 and perl(Cwd::Guard)=0.05. It checks
scoped and nested directory restoration, directory-descriptor restoration to
the same inode after renaming, and original undefined-return plus
$Cwd::Guard::Error behavior on an unavailable directory. It uses installed
modules only, never adds File::Spec::Link as a smoke/runtime dependency.
The failure API returns undef, not an exception; no false success-time Error
reset guarantee is imposed.

These are ordinary functional QEMU-user checks, not native RISC-V,
performance/timing, privilege/security or concurrent-filesystem claims.
Repository metadata/unit/Golden/Dashboard and checksum-only cached source
verification do not execute upstream tests and cannot establish target
success. Protected-main merge/publication remains separately trust-gated;
no public RPM/SRPM addresses or passing target result are invented.
