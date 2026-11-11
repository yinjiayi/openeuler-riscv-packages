# Stagit 1.3

Official origin: <https://codemadness.org/stagit.html>, delegated release index
<https://codemadness.org/releases/stagit/>. The fixed 19,845-byte archive has
SHA256 `a265be67d2c5639094643f16c81d817c626d7557ed7886c9310a1ba317237f8d`,
matching its advertised official checksum. The observed complete index has no
release-signature links; the general homepage PGP-key link is not a signature
for this archive. No independent signature verification is claimed.

The AUR lineage is Stagit 1.2-1; official stable 1.3 is selected from the observed
release index, rather than editing catalog data or downgrading source.

The original Makefile `all` builds both `stagit` and `stagit-index`, always linked
with the three original compatibility objects. Only system compiler/link flags
and standard libgit2 include/library paths replace `/usr/local` defaults. The
original install target installs both executables, both manuals, README, CSS,
two images and both example scripts. Examples stay documentation, not new PATH
commands. No default feature or tests are removed; upstream ships no check/test
target or regression fixtures. No source patches are applied.

The application LICENSE is MIT; the always-linked reallocarray/strlcat/strlcpy
contain ISC grants. All four complete notices are installed for each binary
subpackage. The tests package also retains the unchanged full 16-file source
archive. Authored QA has its complete MIT grant/disclaimer in the installed file.

Target-only QA creates a private local Git repository with deterministic commits,
text/binary content, tags and metadata. It checks both tools, HTML escaping,
file/commit/reference pages, Atom feeds, cache rerun, log limiting and selected
negative CLI paths. It runs against built and staged tools in `%check`, and the
installed tools through smoke. No external network, example hook or clone is
used. Metadata requests `network_during_build: false`; this is not proof that a
CI container has network isolation. No package source, authored QA, compiler,
RPM or QEMU is executed on the packaging host. Target build, real installed
dependency/namespace and native-hardware acceptance remain separate CI gates.
