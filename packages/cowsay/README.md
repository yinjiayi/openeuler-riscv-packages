# Cowsay

Cowsay3.8.4 is the maintained cowsay-org project explicitly linked by the
official `https://cowsay.diamonds` homepage. Arch extra supplies discovery
lineage, not the target build source or target dependency evidence. Stable tag
`v3.8.4` resolves to commit `027c9268ac8571408e153214b9cf1a5e6fab0cfc`;
the41,246-byte fixed-commit archive SHA-256 is
`74e78cd8a5d89c60ed4de1dc8211ccb395868234f5ffe2c6cab93088dc5010f2`.
All75 inert archive members matched their complete upstream Git blobs/modes.

The original `make all` is a no-op. The unchanged default `make install` uses
supported `prefix=/usr sysconfdir=/etc DESTDIR=...` overrides and installs both
commands, both manual paths (cowthink is a relative symlink in each case), all
51 default cow files, and the site-cows/configuration directories. No cow,
feature, source notice or original test is removed. `make man` is explicitly an
authoring-time operation upstream: generated manuals are checked in and the
normal build/install does not invoke Asciidoctor.

`GPL-3.0-only` reflects the explicit whole-project GPLv3 grant in README.md,
complete LICENSE.txt, and original-author relicensing recorded for3.04 in
CHANGELOG.md. New contributions may choose the GPL1.0-or-later branch of the
GPL/Artistic policy, compatible with GPLv3. Individual cow and archived Perl
module attribution/unknown-artist notices are retained unchanged; this is not
a blanket license inference for unrelated external artwork or linked cow
collections. Neither external collections nor an external packaging recipe
were fetched as source. Both RPMs carry complete upstream LICENSE.txt; the
tests RPM retains the exact entire unchanged archive and manual checklist.
No detached signature was advertised in the captured homepage or matching
published release assets; no signed-tag claim is made.

There is no original automated suite, test directory, or test/check Makefile
target in this release. Upstream's release checklist calls for manual testing
and exercising every cow. Authored GPLv3 downstream QA follows that intent and
adds executable checks; it is not presented as an upstream suite. `%check`
and installed smoke run the same target-only QA: exact source/license/docs/
manual/script/cow bytes, relative symlinks, all51 cow renderings, default and
thinking balloons, faces, wrapping, stdin preservation, custom selection,
random selection, COWPATH isolation, a private-prefix registry and negative
selection/input cases. The private-prefix mirror exercises supported registry
behavior without writing the installed system's `/etc` or site-cows. Actual
installed default directory and source bindings are checked separately.

Runtime imports are Cwd, File::Basename, File::Find, Getopt::Std, Text::Tabs and
Text::Wrap, supplied by the declared Perl capabilities. Coreutils supplies the
original `/usr/bin/env` shebang. BuildRequires are make, perl, coreutils, tar,
gzip, python3 and bash; tests require exact cowsay, python3 and bash. QA uses
fresh temporary directories and subprocess timeouts, without network or a
compiler. Local preparation never executes upstream Perl or authored QA.
Source/tooling checks do not establish target behavior, native RISC-V,
performance, physical RPM/SRPM, or installation acceptance; those require CI.
