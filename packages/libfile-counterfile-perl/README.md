<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-counterfile-perl

The frozen inventory's Ubuntu `libfile-counterfile-perl` 1.04-7 source maps
to the official stable CPAN File-CounterFile 1.04 release. The HTTPS archive
SHA-256 `3fd6d66ffa92b884fc9feb4f200daf47250570520c6955fdca7e717fd4a6ac1f`
matches the publisher's `CHECKSUMS` entry. Its single-root archive contains
regular source, documentation and test files only, with no traversal paths,
symlinks or special files.

The README and module POD both grant redistribution and modification under
the same terms as Perl itself; no shipped file has a conflicting notice. The
RPM records the standard Perl GPL-1.0-or-later or Artistic-1.0-Perl choice.

The official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(File::CounterFile)` provider and supplies the
used core modules Carp, Fcntl, Symbol and Config. This is a snapshot check,
not a guarantee about later repository changes.

Both unchanged upstream default tests passed locally (2 files, 101 checks).
The `t/race.t` test forks ten children per round for 100 rounds to check
counter increments and file locking; it writes only a `./zz-counter-$$` file
inside the isolated build directory and unlinks it. This checks user-space
functional behavior, not native RISC-V kernel locking, timing or performance.
The installed-RPM smoke uses `File::Temp` to create and clean a private
counter path, then checks increment/decrement values. Exact-head target CI
must still establish RPM build, full tests and installed smoke; PR artifacts
alone do not prove public repository publication.
