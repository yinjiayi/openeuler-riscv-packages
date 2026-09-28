<!-- SPDX-License-Identifier: Apache-2.0 -->
# mujs

This directory packages MuJS 1.3.10 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. MuJS supplies a JavaScript interpreter, a pretty-printer,
and embeddable shared and static C libraries. The official upstream download
index lists 1.3.10 as its newest stable source release. CI retrieves the HTTPS
archive and verifies SHA-256
`6e36c15dbb84ff859320297c900852f241b131a7b6ddaea669ac9a65bd75571c`
before building. Its 58 archive members are regular files or directories
within `mujs-1.3.10/`, with no duplicate or unsafe paths and no links.

The frozen discovery snapshot records MuJS in Arch Extra 1.3.9, Debian
1.3.6, Fedora 44 1.3.7, openSUSE Tumbleweed 1.3.7, and Ubuntu 26.04 1.3.8.
These rows establish distribution lineage; they are not source checksum or
build instructions. No distribution recipe was executed.

The upstream archive includes the ISC license in `COPYING`. Its Makefile has
no registered test target, so `%check` executes JavaScript parsing, object
access, arithmetic, and a pretty-printer round trip. The installed-RPM smoke
also compiles and runs a program against the public C API through pkg-config.
The upstream public header still advertises a 1.3.8 API macro in the 1.3.10
archive; smoke tests use release metadata for the package version and test
actual API behavior.

External source remains under the upstream ISC license. Apache-2.0 covers
only the original packaging metadata, script, and documentation here.
