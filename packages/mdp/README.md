# mdp

Official stable tag `1.0.19` binds commit
`1bd179043ca4f21705ebe89e57c1c5b80101e7d7`. The 50,412-byte fixed official
archive has SHA-256 `59fc010403f63a425b7b31f8b3a6bd8adc6898fcf5349fb9720fdc9b94e893be`;
all 33 regular members match complete Git blob IDs and modes.

Core C/header notices, both Makefiles and the original version output explicitly
permit GPL version 3 or later. This source evidence governs this recipe rather
than Arch's GPL-3.0-only catalog label. Complete COPYING/AUTHORS/CREDITS, the
manual, sample presentation, community documentation and all source/test bytes
are retained. Authored installed QA has a full separate MIT notice; the tests
subpackage accounts for both licenses. The exact lightweight tag, bounded
release list and full tree advertise no detached signature/checksum asset;
this bounded observation is not a global assertion that none exists elsewhere.

Default `make all` compiles all seven C files and links ncursesw. Only standard
compiler/link packaging flags are supplied: overriding upstream `LDFLAGS=-s`
preserves the unstripped executable for normal RPM debuginfo handling. Original
`make install` stages the binary and pregenerated manual with PREFIX/DESTDIR;
no feature, keybinding, color, parser or resize default is changed.

The full original `make test` target runs both unchanged Python PTY suites:
10 comment/metadata cases with 15 checks and 5 resize cases with 9 checks.
The original timings, assertions and PTY resize behavior are preserved.
Downstream checks require the real exit status, exact full-pass summaries and
no executed FAIL lines. The installed smoke extracts the complete retained
source into a private directory, points its otherwise absent `mdp` path to the
installed binary and invokes both original scripts without compilation.
TERM=xterm and private HOME/TMPDIR make target execution deterministic while
leaving LINES/COLUMNS unset for real PTY resizing. CLI version/help (upstream
help intentionally exits 1), invalid numeric input and missing-file checks are
additional assertions, not replacements for either suite.

All functional source, original PTY tests and authored QA execute only in target
CI; local work is limited to inert review, metadata validation, trusted tooling
tests, golden checks and offline source verification. Source-level dependency
and namespace admission is not a target build/install or physical-product pass.
No native RISC-V hardware, security isolation or production reliability claim.
