<!-- SPDX-License-Identifier: Apache-2.0 -->
# 9menu

Packages official 1.11 tag commit baa949d59ff875b8f9863e26c7b422b6985edff6.
Debian 1.11-1 is a discovery clue, not an upstream version substitution or frozen
catalog entry. All eight archive members were read and SHA-256 bound.

The payload uses exact custom upstream README terms, represented accurately as
LicenseRef-9menu; this is not MIT, an OSI listing, or an independent legal approval.
Keep the copyright/license notices and recipients' awareness; upstream conditions
on unapproved functionality changes remain applicable. No functionality patch is
included. Both packages retain the exact README as license notice. The repository
license covers only original packaging metadata, QA and this documentation.

Regenerate original Imakefile with actual target xmkmf, preserving default all,
install, install.man and CPP manpage transformation. The supplied generated
Makefile targets ancient i386; it is not executed. An exact byte copy from original
9menu.1 to 9menu.man supplies the filename expected by original Imake rules.
Standard RPM flags/paths/modes defer stripping and install section1 explicitly.

There is no original test/check target; none is removed or bypassed. Mandatory
private-Xvfb QA runs the built, staged and installed executable and covers exact
CLI contracts, default font fallback, keyboard/mouse distinct command effects,
file/stdin options, popup shell fallback/exit status, exec replacement and owned
cleanup. Exact original notice/docs plus installed manpage semantics are checked.
No local source/compiler/target/RPM/QEMU execution was used. Target execution,
ordinary installation, complete exact-head CI and physical RPM/SRPM remain gates.

Release 2 changes downstream QA synchronization only: the four existing bounded
waits require expected command-marker bytes, not merely file existence. Original
15-second limits, polling interval, commands, final assertions and upstream source
are unchanged. Shell redirection can create a file before printf completes; the
failed M130 installed assertion did not record marker contents, so this is not
proof of a unique failure cause or a transient-infrastructure diagnosis. The
follow-up still requires its own exact-head target build, installed QA, ordinary
DNF and physical RPM/SRPM acceptance; static inspection is not target success.
