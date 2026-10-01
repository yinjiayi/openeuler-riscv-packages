<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-data-perl

The frozen inventory's `libfile-data-perl` key records Ubuntu source 1.20-5.
This package uses the official [File-Data 1.20](https://metacpan.org/dist/File-Data)
CPAN release. The HTTPS archive SHA-256
`2fe90c9272199e2e112b4d7ae2aae267d282ccec78168cfd4f048e3317940e57`
matches the publisher's `CHECKSUMS` entry. Its single-root archive contains
only regular files and directories, with no traversal or links. The module
POD grants redistribution under Perl 5 terms; no archive file has a
conflicting notice. The RPM uses the repository's Perl 5 dual-license SPDX
mapping, `GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Data` nor `perl(File::Data)`. It supplies the
declared Carp 1.50, Data::Dumper 2.183, Fcntl 1.15 and FileHandle 2.05
providers, all above upstream's minimum versions. This is a snapshot check,
not a guarantee about future repository contents.

Carp's upstream minimum is 1.3301. Perl considers 1.50 newer, but RPM's
version ordering considers `1.50` older than `1.3301`; using that Perl
minimum verbatim in a versioned RPM virtual dependency prevented DNF from
installing the target's `perl-Carp` 1.50. The SPEC therefore requires the
known target RPM version at build and runtime, and independently checks
`Carp->VERSION(1.3301)` with Perl in `%check`. This preserves the upstream
minimum without relying on incompatible version-ordering rules.

Upstream Makefile.PL installs the module under `File/File/Data.pm` because
`INST_LIBDIR` already includes the `File` subdirectory. The package-local
patch changes the destination to `INST_LIB/File/Data.pm`, without altering
module behavior or tests. A fresh local source build retained upstream's
one default test file and all 16 assertions passed. A separate staged install
after the patch placed `File/Data.pm` at the loadable library path, and Perl
loaded version 1.20 from that stage. The target `%check` and installed-RPM
smoke independently verify the install path. Exact-head target CI must still
prove RPM build, tests and smoke; PR artifacts are not public publication.
