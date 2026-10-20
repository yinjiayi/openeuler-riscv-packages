# Dhex

Dhex 0.69 is Thomas Dettbarn's ncurses hexadecimal editor and two-file diff
viewer. Arch extra 0.69-5 provides discovery lineage, not the build source or a
target supply guarantee. The fixed official HTTPS archive is 57,362 bytes with
SHA-256 `52730bcd1cf16bd4dae0de42531be9a4057535ec61ca38c0804eb8246ea6c41b`.
All 36 regular source members were captured inertly; the official page showed
no detached signature or checksum link. No Git-tree identity is claimed.

The full original `all: dhex`, 13 C objects, ncurses link, embedded GPL display,
interactive editor/diff/search/calculator/correlation functions and default
install remain enabled. Distribution compiler/linker hardening replaces the
hard-coded optimization flag while retaining warnings and original include and
library search paths. Upstream `DESTDIR` means an installation prefix, not a
staging root: the recipe calls the original install with a staged `/usr` prefix
then relocates its four unchanged manuals from `usr/man` to `usr/share/man`.
The original install's `strip dhex` is retained, so no unstripped debug product
is promised. There are no source patches or functionality/test switches.

`GPL-2.0-or-later` follows the actual README and main-program grant, rather than
the catalog's GPL-2.0-only label. Both packages retain complete unchanged gpl.txt
and README.txt notices; `dhex-tests` retains the unchanged official source
archive, including the embedded GPL implementation and all source files.

The captured release contains no test/check target or original test suite;
todo.txt explicitly asks for a future suite. New downstream Apache-2.0 QA is
mandatory for both the just-built and staged binary in `%check`, and for the
installed binary in smoke. Batch checks exercise version/help/license,
ASCII/hex search, reverse search, search-log replay, base-address translation,
two independent file search logs, absent matches and genuine input failures.
Separate mandatory PTY checks use an isolated raw 80x24 terminal and explicit
23-key config: real hex edit/save, edit/undo, edit/discard and two-file diff
navigation/exit, verifying resulting file bytes. No user config is used or
changed. Temporary directories and bounded I/O/process deadlines prevent stale
outputs and hangs; a missing terminal or failed check is a failure, not a skip.

The tests need Python standard-library PTY/termios modules and xterm-256color
terminfo; no compiler, network or source execution is needed at installed test
time. RPM generates shared-library runtime requirements. Provider closure,
fresh canonical/open-PR uniqueness, target build/install and physical RPM/SRPM
acceptance are separate gates; this inert draft proves none of those gates.
