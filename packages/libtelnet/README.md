<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtelnet

This directory packages upstream `https://github.com/seanmiddleditch/libtelnet` version `0.23` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Official release 0.23 is non-draft and non-prerelease, tag commit
`c979e8a9d23cfec82dec81be82c3c8f9139fa04a`. Its original release asset
`libtelnet-0.23.tar.gz` has SHA-256
`d2f01a9dc0cc01777844b6d27f0f836dad9a4b9a32a31c7bbde0762480262f25`.
No detached archive signature or checksum asset is published. The lightweight
tag is unsigned; the referenced commit has a GitHub-verified signature, which
does not constitute an independent signature on the release archive.

`LicenseRef-libtelnet-public-domain` means the explicit dedication in COPYING,
libtelnet.c, libtelnet.h and the utility sources, not a claim that this text is
CC0 or Unlicense. The release also contains Windows-only zlib 1.2.5 headers and
static libraries, covered by their retained Zlib notices; Linux builds never
link those binaries and use the system zlib-devel package. Generated Autotools
helpers retain their original notices and distribution exceptions in the SRPM.
The license files installed with the package preserve COPYING and the complete
zlib header notice.

The generated configure script is used without autoreconf. Default shared and
static libraries, all three utilities, optional compression via system zlib,
and Doxygen documentation are retained. No network fetch is needed to build.
Only libtool's installed .la metadata is omitted by the packaging recipe.

The original default `make check` is retained: Automake registers run-all.sh,
which executes all eleven unchanged .test fixtures through telnet-test and
compares their expected parser output. The package also installs the original
runners/fixtures and the test ELF under libexec; smoke copies the data into a
private writable directory and repeats all eleven comparisons against installed
libraries. These are offline parser tests and never open a network listener or
connect to another host. No upstream source or tests were executed locally.

Admission currently uses the complete official base primary/filelists bound to
repomd SHA-256 `1e7269d6fa08e8f837e0ead13ad324e7f4ee5569dde6691378a61a806145bc14`.
All explicit build/runtime dependencies and their transitive closure were found
there; no supplemental dependency is assumed. Supplemental namespace freshness,
actual target dependency resolution, unprivileged build/default tests,
installation/smoke, and physical RPM/SRPM acceptance remain independent gates.
RISC-V status is unknown until real target CI passes; no patch is currently used.
